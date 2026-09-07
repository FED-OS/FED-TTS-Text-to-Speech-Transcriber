# FED TTS 0.3.0 — Dark mode + Settings + Visual overhaul
## Design & build
- [x] Study current app.py / grammar_checker / auto_transcriber / styles.css
- [x] Create src/fed_tts/ui.py — theme engine (Light/Dark/Auto), accent colors, font scale, hero banner, stat cards, health ring, chips
- [x] Create src/fed_tts/settings.py — persistent settings (JSON, offline)
- [x] auto_transcriber.py: add to_srt() / to_vtt() subtitle export + timestamp interval param
- [x] Rewrite app.py: settings sidebar, hero banner, restyled tabs, Tools tab (stats, find&replace, history), SRT/VTT/TXT downloads, grammar health score
- [x] Fix live-test bug: StreamlitWidgetAlreadyInstantiatedError via deferred-write pattern (set_transcript)
## Verify
- [x] Add tests for srt/vtt, settings, ui components (target: all pass) — 63 passed
- [x] Restart app, live browser test: light mode, dark mode toggle, accent change, save persistence, auto transcribe MP4, subtitles tab, tools tab, find & replace, grammar health ring
- [x] Screenshots of new UI (light + dark) — v030_light.png, v030_final_dark2.png
- [x] Update README/usage/CHANGELOG (0.3.0 entry), package zip, deliver
