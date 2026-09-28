import tkinter as tk
from tkinter import font as tkFont, messagebox
from .encoder import encode_to_image
from .decoder import decode_from_image

def launch_app():
    root = tk.Tk()
    root.title("Rangoli Codec Studio")
    root.geometry("500x320")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Enter text to encode into Rangoli:", font=("Helvetica", 11, "bold")).pack(anchor="w")
    entry = tk.Entry(frame, width=45, font=("Helvetica", 12))
    entry.pack(pady=8, ipady=4, fill="x")

    status = tk.Label(frame, text="Ready", fg="#666", font=("Helvetica", 10))
    status.pack(pady=4)

    def on_generate():
        text = entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text first.")
            return
        status.config(text="Generating & Displaying...", fg="blue")
        root.update_idletasks()
        try:
            encode_to_image(text, "preview_rangoli.png", show=True)
            status.config(text="Render complete! Saved to preview_rangoli.png", fg="green")
        except Exception as err:
            status.config(text=f"Error: {err}", fg="red")

    def on_decode():
        try:
            decoded = decode_from_image("preview_rangoli.png")
            messagebox.showinfo("Decoded Content", f"Decoded Text:\n\n{decoded}")
        except Exception as err:
            messagebox.showerror("Decode Error", str(err))

    btn_generate = tk.Button(
        frame, text="Encode & View Rangoli", font=("Helvetica", 11, "bold"),
        bg="#2E7D32", fg="white", padx=10, pady=6, command=on_generate
    )
    btn_generate.pack(pady=8, fill="x")

    btn_decode = tk.Button(
        frame, text="Decode Current Preview Image", font=("Helvetica", 10),
        bg="#1565C0", fg="white", padx=10, pady=4, command=on_decode
    )
    btn_decode.pack(pady=4, fill="x")

    root.mainloop()

if __name__ == "__main__":
    launch_app()