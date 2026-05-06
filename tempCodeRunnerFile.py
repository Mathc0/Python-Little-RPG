play_music(file_path):
    """Charge et joue une musique en boucle."""
    if SOUND_ENABLED and os.path.exists(file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(-1)  # -1 pour jouer en boucle indéfiniment
        except pygame.error as e:
            print(f"Impossible de jouer la musique {file_p