const { createApp } = Vue;

const STORAGE_KEY = "notas.importantes";

const app = createApp({
  data() {
    return {
      notes: [],
      form: {
        title: "",
        content: "",
        tags: "",
        dueDate: "",
      },
      filters: {
        search: "",
        tag: "",
      },
    };
  },
  computed: {
    filteredNotes() {
      return this.notes
        .filter((note) => !note.archived)
        .filter((note) => {
          if (!this.filters.tag.trim()) return true;
          return note.tags.includes(this.filters.tag.trim().toLowerCase());
        })
        .filter((note) => {
          if (!this.filters.search.trim()) return true;
          const term = this.filters.search.toLowerCase();
          return (
            note.title.toLowerCase().includes(term) ||
            note.content.toLowerCase().includes(term)
          );
        });
    },
    archivedNotes() {
      return this.notes.filter((note) => note.archived);
    },
  },
  created() {
    this.loadNotes();
  },
  methods: {
    loadNotes() {
      const raw = localStorage.getItem(STORAGE_KEY);
      this.notes = raw ? JSON.parse(raw) : [];
    },
    saveNotes() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.notes));
    },
    addNote() {
      const newNote = {
        id: crypto.randomUUID(),
        title: this.form.title,
        content: this.form.content,
        tags: this.form.tags
          ? this.form.tags
              .split(",")
              .map((tag) => tag.trim().toLowerCase())
              .filter(Boolean)
          : [],
        dueDate: this.form.dueDate || null,
        createdAt: new Date().toISOString(),
        archived: false,
      };
      this.notes.unshift(newNote);
      this.saveNotes();
      this.form.title = "";
      this.form.content = "";
      this.form.tags = "";
      this.form.dueDate = "";
    },
    archiveNote(id) {
      const note = this.notes.find((item) => item.id === id);
      if (note) {
        note.archived = true;
        this.saveNotes();
      }
    },
    clearFilters() {
      this.filters.search = "";
      this.filters.tag = "";
    },
    formatDate(value) {
      if (!value) return "";
      return new Date(value).toLocaleString("es-ES", {
        dateStyle: "medium",
        timeStyle: "short",
      });
    },
  },
});

app.mount("#app");
