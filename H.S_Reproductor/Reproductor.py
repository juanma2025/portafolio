import tkinter as tk
from tkinter import filedialog, messagebox
import pygame  # We use pygame for audio playback

# Class for the node of the doubly linked list
class Node:
    def __init__(self, song):
        self.song = song  # Song data (file name)
        self.next = None  # Reference to the following node
        self.prev = None  # Reference to previous node

# Type of the doubly linked list
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def append(self, song):
        """Agrega una canción al final de la lista."""
        new_node = Node(song)
        if self.head is None:  # The list is empty
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def play_next(self):
        """Avanza a la siguiente canción."""
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.song
        return None

    def play_previous(self):
        """Retrocede a la canción anterior."""
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.song
        return None

    def start(self):
        """Inicia la reproducción desde la primera canción."""
        self.current = self.head
        if self.current:
            return self.current.song
        return None

# Music player class with graphical interface
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x300")

        # Playlist configuration
        self.playlist = DoublyLinkedList()

        # Inicializamos pygame mixer
        pygame.mixer.init()

        # Controles de la interfaz
        self.song_label = tk.Label(root, text="No song playing", font=("Helvetica", 14))
        self.song_label.pack(pady=20)

        # Botones de control
        control_frame = tk.Frame(root)
        control_frame.pack(pady=20)

        play_button = tk.Button(control_frame, text="Play", command=self.play_song)
        play_button.grid(row=0, column=0, padx=10)

        pause_button = tk.Button(control_frame, text="Pause", command=self.pause_song)
        pause_button.grid(row=0, column=1, padx=10)

        next_button = tk.Button(control_frame, text="Next", command=self.play_next_song)
        next_button.grid(row=0, column=2, padx=10)

        prev_button = tk.Button(control_frame, text="Previous", command=self.play_previous_song)
        prev_button.grid(row=0, column=3, padx=10)

        add_song_button = tk.Button(root, text="Add Song", command=self.add_song)
        add_song_button.pack(pady=10)

    def add_song(self):
        """Agregar una canción a la lista de reproducción."""
        song = filedialog.askopenfilename(title="Select a song", filetypes=(("mp3 files", "*.mp3"),))
        if song:
            self.playlist.append(song)
            messagebox.showinfo("Song Added", f"Added {song} to the playlist!")

    def play_song(self):
        """Reproduce la primera canción de la lista."""
        song = self.playlist.start()
        if song:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            self.song_label.config(text=f"Playing: {song}")
        else:
            messagebox.showwarning("No Songs", "No songs in the playlist!")

    def pause_song(self):
        """Pausa o reanuda la reproducción de la canción."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def play_next_song(self):
        """Reproduce la siguiente canción en la lista."""
        song = self.playlist.play_next()
        if song:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            self.song_label.config(text=f"Playing: {song}")

    def play_previous_song(self):
        """Reproduce la canción anterior en la lista."""
        song = self.playlist.play_previous()
        if song:
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            self.song_label.config(text=f"Playing: {song}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
