from telethon.tl.custom.button import Button

def get_control_buttons():
    return [
        [
            Button.inline("⏸ Pause", b"pause"),
            Button.inline("▶️ Resume", b"resume"),
        ],
        [
            Button.inline("⏭ Seek +10s", b"seek_forward"),
            Button.inline("⏮ Seek -10s", b"seek_backward"),
        ],
        [
            Button.inline("⏹ Stop", b"end"),
            Button.inline("❌ Close", b"close"),
        ]
    ]
