#!/usr/bin/env python3
import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

DATA_PATH = Path(__file__).resolve().parent / "data" / "notes.json"


@dataclass
class Note:
    id: int
    title: str
    content: str
    tags: List[str]
    created_at: str
    due_date: Optional[str] = None
    archived: bool = False


def load_notes() -> List[Note]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [Note(**item) for item in payload]


def save_notes(notes: List[Note]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as handle:
        json.dump([asdict(note) for note in notes], handle, ensure_ascii=False, indent=2)


def next_id(notes: List[Note]) -> int:
    return max((note.id for note in notes), default=0) + 1


def add_note(args: argparse.Namespace) -> None:
    notes = load_notes()
    note = Note(
        id=next_id(notes),
        title=args.title.strip(),
        content=args.content.strip(),
        tags=[tag.strip() for tag in args.tags.split(",") if tag.strip()] if args.tags else [],
        created_at=datetime.now().isoformat(timespec="seconds"),
        due_date=args.due,
    )
    notes.append(note)
    save_notes(notes)
    print(f"Nota creada con ID {note.id}.")


def list_notes(args: argparse.Namespace) -> None:
    notes = [note for note in load_notes() if not note.archived]
    if args.tag:
        notes = [note for note in notes if args.tag in note.tags]
    if args.search:
        term = args.search.lower()
        notes = [
            note
            for note in notes
            if term in note.title.lower() or term in note.content.lower()
        ]
    if not notes:
        print("No hay notas para mostrar.")
        return

    for note in notes:
        tags = f" [tags: {', '.join(note.tags)}]" if note.tags else ""
        due = f" (vence: {note.due_date})" if note.due_date else ""
        print(f"#{note.id} {note.title}{tags}{due}\n  {note.content}\n")


def archive_note(args: argparse.Namespace) -> None:
    notes = load_notes()
    for note in notes:
        if note.id == args.id:
            note.archived = True
            save_notes(notes)
            print(f"Nota #{args.id} archivada.")
            return
    print(f"No se encontró la nota con ID {args.id}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sistema simple para guardar notas importantes.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Agregar una nota nueva")
    add_parser.add_argument("title", help="Título corto de la nota")
    add_parser.add_argument("content", help="Detalle o recordatorio")
    add_parser.add_argument("--tags", help="Etiquetas separadas por coma")
    add_parser.add_argument("--due", help="Fecha límite (YYYY-MM-DD)")
    add_parser.set_defaults(func=add_note)

    list_parser = subparsers.add_parser("list", help="Listar notas")
    list_parser.add_argument("--tag", help="Filtrar por etiqueta")
    list_parser.add_argument("--search", help="Buscar por texto")
    list_parser.set_defaults(func=list_notes)

    archive_parser = subparsers.add_parser("archive", help="Archivar una nota")
    archive_parser.add_argument("id", type=int, help="ID de la nota")
    archive_parser.set_defaults(func=archive_note)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
