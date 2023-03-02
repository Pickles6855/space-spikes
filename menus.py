import main
import pygame
from sys import exit as sysexit
from os.path import join as os_path_join

class Button:
    def __init__(self, x, y, width, height, img, hover_img, click_func):
        self.rect = pygame.Rect(x, y, width, height)
        self.img = img
        self.hover_img = hover_img
        self.display_img = self.img
        self.click_func = click_func
        self.already_clicked = False

    def process(self, events=pygame.event.get()):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.display_img = self.hover_img
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and self.already_clicked == False:
                    self.click_func()
                    self.already_clicked = True
                    if main.sound == True:
                        main.ui_channel.play(main.CLICK_SOUND)

        else:
            self.display_img = self.img
            self.already_clicked = False

def death_screen(score, highscore, bg, mg, fg, spikes, screen_powerups, current_frame, player):
    global is_dead
    main.save_data(highscore, main.music, main.sound)
    # Load images
    DEATH_SCREEN_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/death_screen.png'), (256, 192)).convert_alpha()
    MENU_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/menu.png'), (96, 30)).convert_alpha()
    MENU_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/menu_hover.png'), (96, 30)).convert_alpha()
    RESTART_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/restart.png'), (96, 30)).convert_alpha()
    RESTART_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/restart_hover.png'), (96, 30)).convert_alpha()

    
    prev_screen = main.get_prev_screen(bg, mg, fg, spikes, screen_powerups, current_frame, player)
    
    for i in range(main.HEIGHT//2 - 192//2):
        main.WIN.blit(prev_screen, (0, 0))
        main.WIN.blit(DEATH_SCREEN_IMG, (main.WIDTH/2 - 256/2, i))
        pygame.display.update()

        
    restart_button = Button(main.WIDTH//2 - 96//2, main.HEIGHT//2 + 10, 96, 30, RESTART_BUTTON_IMG, RESTART_BUTTON_HOVER_IMG, main.restart)
    menu_button = Button(main.WIDTH//2 - 96//2, main.HEIGHT//2 + 50, 96, 30, MENU_BUTTON_IMG, MENU_BUTTON_HOVER_IMG, title_screen)
    buttons = [menu_button, restart_button]

    
    is_dead = True
    death_screen_fps_clock = pygame.time.Clock()
    while is_dead:
        death_screen_fps_clock.tick(main.FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        main.WIN.blit(prev_screen, (0, 0))
        main.WIN.blit(DEATH_SCREEN_IMG, (main.WIDTH/2 - 256/2, main.HEIGHT//2 - 192//2))

        score_text = main.PRESSSTART2P_FONT_SMALL.render(f'Score:{score}', True, (100, 100, 120))
        high_score_text = main.PRESSSTART2P_FONT_SMALL.render(f'Best:{highscore}', True, (100, 100, 120))
        main.WIN.blit(score_text, (main.WIDTH//2 - score_text.get_width()//2, main.HEIGHT//2 - 37))
        main.WIN.blit(high_score_text, (main.WIDTH//2 - score_text.get_width()//2, main.HEIGHT//2 - 17))

        [button.process(events=events) for button in buttons]

        [main.WIN.blit(button.display_img, button.rect) for button in buttons]
        
        pygame.display.update()


def pause_screen(bg, mg, fg, spikes, screen_powerups, current_frame, player):
    global paused
    main.save_data(main.highscore, main.music, main.sound)

    PAUSE_SCREEN_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/pause_screen.png'), (256, 192)).convert_alpha()
    MENU_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/menu.png'), (96, 30)).convert_alpha()
    MENU_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/menu_hover.png'), (96, 30)).convert_alpha()
    RESUME_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/resume.png'), (96, 30)).convert_alpha()
    RESUME_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/resume_hover.png'), (96, 30)).convert_alpha()
    SOUND_ON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_on.png'), (35, 35)).convert_alpha()
    SOUND_OFF_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_off.png'), (35, 35)).convert_alpha()
    SOUND_ON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_on_hover.png'), (35, 35)).convert_alpha()
    SOUND_OFF_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_off_hover.png'), (35, 35)).convert_alpha()
    MUSIC_ON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_on.png'), (35, 35)).convert_alpha()
    MUSIC_OFF_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_off.png'), (35, 35)).convert_alpha()
    MUSIC_ON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_on_hover.png'), (35, 35)).convert_alpha()
    MUSIC_OFF_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_off_hover.png'), (35, 35)).convert_alpha()

    prev_screen = main.get_prev_screen(bg, mg, fg, spikes, screen_powerups, current_frame, player)

    resume_button = Button(main.WIDTH//2 - 96//2, main.HEIGHT//2 + 10, 96, 30, RESUME_BUTTON_IMG, RESUME_BUTTON_HOVER_IMG, unpause)
    menu_button = Button(main.WIDTH//2 - 96//2, main.HEIGHT//2 + 50, 96, 30, MENU_BUTTON_IMG, MENU_BUTTON_HOVER_IMG, title_screen)
    sound_button = Button(main.WIDTH//2 - 45, main.HEIGHT//2 - 35, 35, 35, 'img', 'hover_img', toggle_sound)
    music_button = Button(main.WIDTH//2 + 10, main.HEIGHT//2 - 35, 35, 35, 'img', 'hover_img', toggle_music)
    
    buttons = [menu_button, resume_button, sound_button, music_button]

    paused = True
    pause_screen_fps = pygame.time.Clock()
    while paused:
        pause_screen_fps.tick(main.FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        main.WIN.blit(prev_screen, (0, 0))
        main.WIN.blit(PAUSE_SCREEN_IMG, (main.WIDTH/2 - 256/2, main.HEIGHT//2 - 192//2))

        [button.process(events=events) for button in buttons]

        [main.WIN.blit(button.display_img, button.rect) for button in buttons[0:2]]
        if main.sound == True:
            if buttons[2].display_img == buttons[2].hover_img:
                sound_img = SOUND_ON_HOVER_IMG
            else:
                sound_img = SOUND_ON_IMG     
        else:
            if buttons[2].display_img == buttons[2].hover_img:
                sound_img = SOUND_OFF_HOVER_IMG
            else:
                sound_img = SOUND_OFF_IMG
            
        if main.music == True:
            if buttons[3].display_img == buttons[3].hover_img:
                music_img = MUSIC_ON_HOVER_IMG
            else:
                music_img = MUSIC_ON_IMG
        else:
            if buttons[3].display_img == buttons[3].hover_img:
                music_img = MUSIC_OFF_HOVER_IMG
            else:
                music_img = MUSIC_OFF_IMG
            
        main.WIN.blit(sound_img, buttons[2].rect)
        main.WIN.blit(music_img, buttons[3].rect)
        
            
        
        pygame.display.update()
        
        


def unpause():
    global paused
    paused = False
    main.crash_channel.unpause()
    main.gameplay_channel.unpause()
    main.thruster_channel.unpause()

def toggle_sound():
    main.sound = not main.sound
    main.save_data(main.highscore, main.music, main.sound)

def toggle_music():
    main.music = not main.music
    main.save_data(main.highscore, main.music, main.sound)
    
def title_screen():
    global on_title_screen, paused, is_dead
    paused = False
    is_dead = False

    TITLE_OVERLAY_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/title_overlay.png'), (main.WIDTH, main.HEIGHT)).convert_alpha()
    TITLE_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/title.png'), (500, 125)).convert_alpha()
    PLAY_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/play.png'), (144, 45)).convert_alpha()
    PLAY_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/play_hover.png'), (144, 45)).convert_alpha()
    QUIT_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/quit.png'), (144, 45)).convert_alpha()
    QUIT_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/quit_hover.png'), (144, 45)).convert_alpha()
    SOUND_ON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_on.png'), (50, 50)).convert_alpha()
    SOUND_OFF_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_off.png'), (50, 50)).convert_alpha()
    SOUND_ON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_on_hover.png'), (50, 50)).convert_alpha()
    SOUND_OFF_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/sound_off_hover.png'), (50, 50)).convert_alpha()
    MUSIC_ON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_on.png'), (50, 50)).convert_alpha()
    MUSIC_OFF_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_off.png'), (50, 50)).convert_alpha()
    MUSIC_ON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_on_hover.png'), (50, 50)).convert_alpha()
    MUSIC_OFF_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/music_off_hover.png'), (50, 50)).convert_alpha()
    HELP_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/help.png'), (35, 35)).convert_alpha()
    HELP_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/help_hover.png'), (35, 35)).convert_alpha()

    play_button = Button(main.WIDTH//2 - 144//2, main.HEIGHT - 200, 144, 45, PLAY_BUTTON_IMG, PLAY_BUTTON_HOVER_IMG, play)
    quit_button = Button(main.WIDTH//2 - 144//2, main.HEIGHT - 130, 144, 45, QUIT_BUTTON_IMG, QUIT_BUTTON_HOVER_IMG, exit_game)
    help_button = Button(main.WIDTH - 40, main.HEIGHT - 80, 35, 35, HELP_BUTTON_IMG, HELP_BUTTON_HOVER_IMG, tutorial)
    sound_button = Button(main.WIDTH//2 - 65, main.HEIGHT - 60, 50, 50, 'img', 'hover_img', toggle_sound)
    music_button = Button(main.WIDTH//2 + 15, main.HEIGHT - 60, 35, 50, 'img', 'hover_img', toggle_music)
    buttons = [play_button, quit_button, help_button, sound_button, music_button]
    
    title_fps = pygame.time.Clock()
    on_title_screen = True
    while on_title_screen:
        title_fps.tick(main.FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        [button.process(events=events) for button in buttons]

        main.WIN.blit(main.STARS_BG_IMG, (0, 0))

        [main.WIN.blit(button.display_img, button.rect) for button in buttons[0:3]]
        
        if main.sound == True:
            if buttons[3].display_img == buttons[3].hover_img:
                sound_img = SOUND_ON_HOVER_IMG
            else:
                sound_img = SOUND_ON_IMG     
        else:
            if buttons[3].display_img == buttons[3].hover_img:
                sound_img = SOUND_OFF_HOVER_IMG
            else:
                sound_img = SOUND_OFF_IMG
            
        if main.music == True:
            if buttons[4].display_img == buttons[4].hover_img:
                music_img = MUSIC_ON_HOVER_IMG
            else:
                music_img = MUSIC_ON_IMG
        else:
            if buttons[4].display_img == buttons[4].hover_img:
                music_img = MUSIC_OFF_HOVER_IMG
            else:
                music_img = MUSIC_OFF_IMG
            
        main.WIN.blit(sound_img, buttons[3].rect)
        main.WIN.blit(music_img, buttons[4].rect)

        highscore_text = main.PRESSSTART2P_FONT_MED.render(f'High: {main.highscore}', True, (230, 230, 255))
        main.WIN.blit(highscore_text, (main.WIDTH//2 - highscore_text.get_width()//2, main.HEIGHT - 250))
        
        main.WIN.blit(TITLE_OVERLAY_IMG, (0, 0))

        main.WIN.blit(TITLE_IMG, (main.WIDTH//2 - 500//2, 75))
        
        pygame.display.update()


def play():
    global on_title_screen, is_dead
    on_title_screen = False
    if is_dead:
        main.restart()
    main.save_data(main.highscore, main.music, main.sound)

def tutorial():
    global on_tutorial
    print('tutorial')
    MENU_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/menu.png'), (144, 45)).convert_alpha()
    MENU_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{main.DIRECTORY}/Assets/UI/buttons/menu_hover.png'),(144, 45)).convert_alpha()
    menu_button = Button(main.WIDTH//2 - 144//2, main.HEIGHT - 80, 144, 45, MENU_BUTTON_IMG, MENU_BUTTON_HOVER_IMG, exit_tutorial)

    tutorial_text_str = ['Navigate your alien friend through',
                    'the deadly spikes of space.',
                    'Use W and S or the up and down',
                    'arrows to control the spaceship.',
                    'Click on purple powerups to collect',
                    'them and then press space to use',
                    'them. Get the highest score you',
                    'can and good luck!'
    
    ]
    
    tutorial_fps = pygame.time.Clock()
    on_tutorial = True
    while on_tutorial:
        tutorial_fps.tick(main.FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                exit_game()

        main.WIN.blit(main.STARS_BG_IMG, (0, 0))

        tutorial_texts = [main.PRESSSTART2P_FONT_SMALL.render(text, True, (230, 230, 255)) for text in tutorial_text_str]
        
        text_y = 30
        for text in tutorial_texts:
            main.WIN.blit(text, (main.WIDTH//2 - text.get_width()//2, text_y))
            text_y += 50


        menu_button.process(events=events)
        main.WIN.blit(menu_button.display_img, menu_button.rect)
        pygame.display.update()

def exit_tutorial():
    global on_tutorial
    on_tutorial = False

def exit_game():
    pygame.quit()
    quit()