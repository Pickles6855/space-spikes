# Import modules
import pygame
import menus
import other
from sys import exit as sysexit
from os.path import split as os_path_split
from random import randint, choice

DIRECTORY = os_path_split(__file__)[0]

def save_data(highscore1, music1, sound1):
    with open(f'{DIRECTORY}/data.txt', 'w') as data:
        num_of_spaces = 6 - len(str(highscore1))
        spaces = ''
        for i in range(num_of_spaces + 1):
            spaces += ' '
        data.write(f'{highscore1}{spaces}high score\n')
        data.write(f'{music1}  music\n')
        data.write(f'{sound1}  sound')

    global highscore, music, sound
    with open(f'{DIRECTORY}/data.txt', 'r') as data:
        highscore = int(data.readline()[0:5])
        music = eval(data.readline()[0:5])
        sound = eval(data.readline()[0:5])

        if sound == True:
            crash_channel.set_volume(0.5)
            gameplay_channel.set_volume(0.5)
            thruster_channel.set_volume(0.5)
            ui_channel.set_volume(0.5)
        else:
            crash_channel.set_volume(0.0)    
            gameplay_channel.set_volume(0.0)
            thruster_channel.set_volume(0.0)
            ui_channel.set_volume(0.0)

        if music == True:
            pygame.mixer.music.set_volume(0.25)
        else:
            pygame.mixer.music.set_volume(0.0)


with open(f'{DIRECTORY}/data.txt', 'r') as data:
    highscore = int(data.readline()[0:5])
    music = eval(data.readline()[0:5])
    sound = eval(data.readline()[0:5])

pygame.init()

# A powerup class to easily keep track of powerups
class Powerup:
    def __init__(self, type, duration, img):
        self.type = type
        self.duration = duration
        self.img = img

    # The function called to start the specified type of powerup
    def start(self):
        global scroll_vel, collision, thruster_vel
        if self.type == 'slow_down':
            scroll_vel -= 1
        if self.type == 'no_collision':
            collision = False
        if self.type == 'thruster_speed':
            thruster_vel += 1

        if sound == True:
            gameplay_channel.play(ACTIVATE_POWERUP_SOUND)


    # The function called to end the specified type of powerup
    def reset(self):
        global scroll_vel, collision, thruster_vel, powerup_bar_time
        if self.type == 'slow_down':
            scroll_vel += 1
        if self.type == 'no_collision':
            collision = True
        if self.type == 'thruster_speed':
            thruster_vel -= 1

        powerup_bar_time = 0

        if sound == True:
            gameplay_channel.play(DEACTIVATE_POWERUP_SOUND)

pass

# A function that will handle the player movement including checking for key presses and moving the player
def player_movement():
    global current_state, prev_state, thruster_anim
    keys = pygame.key.get_pressed()

    # current_state variable is for knowing when the player is moving for animation
    prev_state = current_state
    
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y >= 0:
        player.y -= thruster_vel
        current_state = 'moving'
    
    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y <= HEIGHT - 100:
        player.y += thruster_vel
        current_state = 'moving'

    # Will keep fire animation visible after the player has stopped moving for a short amount of time for when they move breifly
    if (current_state == 'moving') and not (keys[pygame.K_w] or keys[pygame.K_UP]
                                  or keys[pygame.K_s] or keys[pygame.K_DOWN]):
        thruster_anim += 1
        if thruster_anim >= 40:
            current_state = 'idle'


pass

# A function to check if the player has been hit and if so, trigger the SPIKE_HIT event
def check_for_hit():
    global collision

    # Will only check for collision if the player does not have the powerup 'no collision' activated
    if collision == True:
        # Goes through each of the spikes and checks to see if they have been hit
        for spike in spikes:
            colide_test_rect = pygame.Rect(spike.rect.x + 25, spike.rect.y, spike.rect.width - 25, spike.rect.height)
            if player.colliderect(colide_test_rect) == True:
                # Posts the event SPIKE_HIT to trigger the end of the game
                pygame.event.post(spike_hit_event)

    # Gets the x and y coordinates of the player's mouse
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]

    # For every powerup i the screen, it will check to see if the mouse is overlapping it and if the player has clicked
    for powerup in screen_powerups:
        mouse_collided = pygame.Rect(mouse_x, mouse_y, 1, 1).colliderect(powerup)
        # Checks to see if the left mouse button has been pressed
        if mouse_collided == True and pygame.mouse.get_pressed()[0] == True:
            screen_powerups.remove(powerup)
            pygame.event.post(gain_powerup_event)


        
    


#Variables

pass
##############################################

# Variables
WIDTH, HEIGHT = 500, 500
FPS = 45


# Load in the press start 2p font
PRESSSTART2P_FONT = pygame.font.Font(f'{DIRECTORY}/Assets/UI/PressStart2P.ttf', 32)
PRESSSTART2P_FONT_UNDERLINE = pygame.font.Font(f'{DIRECTORY}/Assets/UI/PressStart2P.ttf', 32)
PRESSSTART2P_FONT_UNDERLINE.set_underline(True)
PRESSSTART2P_FONT_SMALL = pygame.font.Font(f'{DIRECTORY}/Assets/UI/PressStart2P.ttf', 14)
PRESSSTART2P_FONT_MED = pygame.font.Font(f'{DIRECTORY}/Assets/UI/PressStart2P.ttf', 24)


# Setup the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Spikes Pygame')

# Events
# The event for spawning a spike; triggers every few seconds
SPAWN_SPIKE = pygame.USEREVENT + 1
#pygame.time.set_timer(SPAWN_SPIKE, 3750)
spawn_spike_event = pygame.event.Event(SPAWN_SPIKE)

# The event for when the player hits a spike; is not automatically triggered
SPIKE_HIT = pygame.USEREVENT + 2
spike_hit_event = pygame.event.Event(SPIKE_HIT)

# A simple timer event that will trigger every few frames so that you are not constantly updating things like the animations
TIMER_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(TIMER_EVENT, 200)

# This event has a random chance to spawn a powerup everytime it is trigger; triggered every few seconds
SPAWN_POWERUP = pygame.USEREVENT + 4
pygame.time.set_timer(SPAWN_POWERUP, 4000)

# The event for when the player gets a powerup; is not automatically triggered
GAIN_POWERUP = pygame.USEREVENT + 5
gain_powerup_event = pygame.event.Event(GAIN_POWERUP)

# Sets only certain events to be allowed to help with performance
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, SPAWN_SPIKE, SPIKE_HIT, TIMER_EVENT, SPAWN_POWERUP, GAIN_POWERUP, pygame.MOUSEMOTION])


# Load Images
# Main Images
PLAYER_IMG = pygame.image.load(f'{DIRECTORY}/Assets/player_spritesheet.png').convert_alpha()
SPIKE_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/spike.png'), (100, 375)).convert_alpha()

# Background Images
STARS_BG_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/bg/stars.png'), (WIDTH, HEIGHT)).convert()
PLANET_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/bg/planet.png'), (WIDTH, HEIGHT))
BG_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/bg/bg.png'), (WIDTH + 4, HEIGHT)).convert_alpha()
MG_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/bg/mg.png'), (WIDTH + 4, HEIGHT)).convert_alpha()
FG_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/bg/fg.png'), (WIDTH + 4, HEIGHT)).convert_alpha()


# UI Images
POWERUP_BAR_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/UI/powerup_bar.png'), (180, 70)).convert_alpha()
POWERUP_TIMER_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/UI/powerup_timer.png'), (96, 30)).convert_alpha()
PAUSE_BUTTON_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/UI/buttons/pause.png'), (40, 40)).convert_alpha()
PAUSE_BUTTON_HOVER_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/UI/buttons/pause_hover.png'), (40, 40)).convert_alpha()

# Powerup Images
POWERUP_SHEET_IMG = pygame.image.load(f'{DIRECTORY}/Assets/powerups.png').convert_alpha()
POWERUP_IMG = pygame.transform.scale(other.get_frame(POWERUP_SHEET_IMG, 32, 32, 0), (40, 40))
THRUSTER_SPEED_POWERUP_IMG = pygame.transform.scale(other.get_frame(POWERUP_SHEET_IMG, 32, 32, 1), (51, 50))
SLOW_DOWN_POWERUP_IMG = pygame.transform.scale(other.get_frame(POWERUP_SHEET_IMG, 32, 32, 2), (51, 50))
NO_COLLISION_POWERUP_IMG = pygame.transform.scale(other.get_frame(POWERUP_SHEET_IMG, 32, 32, 3), (51, 50))

#SLOW_DOWN_POWERUP_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/powerups/slow_down_powerup.png'), (51, 50))
#THRUSTER_SPEED_POWERUP_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/powerups/thruster_speed_powerup.png'), (51, 50))
#NO_COLLISION_POWERUP_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/powerups/no_collision_powerup.png'), (51, 50))
#POWERUP_IMG = pygame.transform.scale(pygame.image.load(f'{DIRECTORY}/Assets/powerups/powerup.png'), (40, 40)).convert_alpha()


# Load sounds and music
CLICK_SOUND = pygame.mixer.Sound(f'{DIRECTORY}/Assets/sounds/click.wav') # Channel 4 ui
POWERUP_GAIN_SOUND = pygame.mixer.Sound(f'{DIRECTORY}/Assets/sounds/powerup_gain.wav') # Channel 2 powerups
ACTIVATE_POWERUP_SOUND = pygame.mixer.Sound(f'{DIRECTORY}/Assets/sounds/activate_powerup.wav') # Channel 2 powerups
DEACTIVATE_POWERUP_SOUND = pygame.mixer.Sound(f'{DIRECTORY}/Assets/sounds/deactivate_powerup.wav') # Channel 2 powerups
CRASH_SOUND = pygame.mixer.Sound(f'{DIRECTORY}/Assets/sounds/crash.wav') # Channel 1 crash
THRUSTER_SOUND = pygame.mixer.Sound(f'{DIRECTORY}/Assets/sounds/thruster.wav') # Channel 3 thrusters

# Set the number of channels
pygame.mixer.set_num_channels(5)

# Setup various channels to organize the sounds
crash_channel = pygame.mixer.Channel(1)
gameplay_channel = pygame.mixer.Channel(2)
thruster_channel = pygame.mixer.Channel(3)
ui_channel = pygame.mixer.Channel(4)
if sound == True:
    crash_channel.set_volume(0.5)
    gameplay_channel.set_volume(0.5)
    thruster_channel.set_volume(0.5)
    ui_channel.set_volume(0.5)
else:
    crash_channel.set_volume(0.0)
    gameplay_channel.set_volume(0.0)
    thruster_channel.set_volume(0.0)
    ui_channel.set_volume(0.0)

# Music
pygame.mixer.music.load(f'{DIRECTORY}/Assets/sounds/bg_music.wav') # Channel 1 music
if music == True:
    pygame.mixer.music.set_volume(0.25)
else:
    pygame.mixer.music.set_volume(0.0)




def main():
    global player, spikes, current_state, prev_state, thruster_anim, collision, screen_powerups, score, powerup_bar_time, current_frame, powerups, using_powerup, powerup_time, powerup_bar_time, current_powerup, pwrup_tenth_of_bar_reached, highscore, thruster_vel, scroll_vel, bg, mg, fg
    # Initializes and resets the player variables
    # The player rectangle to keep track of position
    player = pygame.Rect(WIDTH / 2 - 50, HEIGHT / 2 - 50, 100, 100)

    # The powerups displayed on the screen that the player can collect
    screen_powerups = []

    # The powerups the player has to use at their disposal
    powerups = []

    # Keeps track of how long the powerup has lasted
    powerup_time = 0

    #Powerup variables for keeping track of the powerup timer
    tnth_of_current_pwrup_duration = None
    powerup_bar_time = 0
    pwrup_tenth_of_bar_reached = 0

    # Other powerup variables
    using_powerup = False
    current_powerup = None
    powerup_chance = 5

    # Other player variables
    collision = True
    score = 0
    new_high_score = False
    show_high_score_msg = True
    shown_high_score_msg = False
    
    # Variable to keep track of when to increase how fast the spikes scroll past; starts at 0 but is imedietly increased to 100
    next_scroll_speed_increase = 0
    
    # Reset the list of spikes
    spikes = []
    spawn_spike_timer = 100

    # The timer variable for the thruster animation
    thruster_anim = 0

    # Other variables for the animation
    current_state = 'idle'
    prev_state = 'idle'
    current_frame = 0

    scroll_vel = 3
    thruster_vel = 3

    # Background
    fg = [pygame.Rect(0, 0, WIDTH + 2, HEIGHT), pygame.Rect(WIDTH, 0, WIDTH, HEIGHT)]
    mg = [pygame.Rect(0, 0, WIDTH, HEIGHT), pygame.Rect(WIDTH, 0, WIDTH, HEIGHT)]
    bg = [pygame.Rect(0, 0, WIDTH, HEIGHT), pygame.Rect(WIDTH, 0, WIDTH, HEIGHT)]

    # Pause button
    pause_button = menus.Button(10, 70, 40, 40, PAUSE_BUTTON_IMG, PAUSE_BUTTON_HOVER_IMG, pause_screen_main)

    crash_channel.unpause()
    gameplay_channel.unpause()
    thruster_channel.unpause()
    ui_channel.unpause()
    

    # Fps
    clock = pygame.time.Clock()
    
    # Game Loop
    running = True
    while running:
        # Fps
        clock.tick(FPS)
        
        # Checks for all the events running/triggered (spawn spike, spike hit, etc.)
        events = pygame.event.get()
        for event in events:

            # For when the player quits the window
            if event.type == pygame.QUIT:
                save_data(highscore, music, sound)
                pygame.quit()
                quit()

            # Spawns two spikes at a random y positions
            if event.type == SPAWN_SPIKE:
                
                # Determines a random y position for the spikes
                spike_y_pos = randint(-350, -150)
                    
                # Creates the top spike
                spikes.append(
                    other.Spike(pygame.Rect(WIDTH + 100, spike_y_pos, 100, 375),
                            SPIKE_IMG, 'top'))
                # Creates the bottom spike
                spikes.append(
                    other.Spike(pygame.Rect(WIDTH + 100, spike_y_pos + 575, 100, 375),
                            pygame.transform.rotate(SPIKE_IMG, 180), 'bottom'))
    
            # For when the player hits a spike and ends the game
            if event.type == SPIKE_HIT:
                crash_channel.play(CRASH_SOUND)
                gameplay_channel.pause()
                thruster_channel.pause()
                menus.death_screen(score, highscore, bg, mg, fg, spikes, screen_powerups, current_frame, player)

            # An event for handling things like animation and using powerups
            if event.type == TIMER_EVENT:
                
                #Animation
                if current_state == 'moving':
                    # Resets the frame if it is one the last one
                    if current_frame >= 4:
                        current_frame = 1
                    # Goes to the next frame
                    current_frame += 1
                
                # Stops the animation if current_state is set to idle
                if current_state == 'idle':
                    current_frame = 0

                if new_high_score:
                    show_high_score_msg = not show_high_score_msg

                save_data(highscore, music, sound)

                    
                #Powerups
                if using_powerup:
                    # If the time since the powerup was started is more than the duration of the powerup, stop using the powerup
                    if powerup_time >= current_powerup.duration:
                        current_powerup.reset()
                        using_powerup = False
                        current_powerup = None
                        
                        # Reset powerup variables for keeping track of the powerup timer
                        powerup_time = 0
                        tnth_of_current_pwrup_duration = 0
                        powerup_bar_time = 0
                        pwrup_tenth_of_bar_reached = 0
                        
                    # Increase how long the powerup has been activated by one
                    powerup_time += 1

                    
            # Checks if various keys are pressed
            if event.type == pygame.KEYDOWN:
                # Checks whether space is pressed and the player has no other powerup activated
                if pygame.key.get_pressed()[pygame.K_SPACE] and using_powerup == False:
                    # The try and except is nessescary in case there is nothing in the powerups list
                    try:
                        # Start using the powerup
                        using_powerup = True
                        current_powerup = powerups[0]
                        powerups.remove(current_powerup)
                        current_powerup.start()
                    except IndexError:
                        using_powerup = False

            # Spawns a powerup
            if event.type == SPAWN_POWERUP:
                # Checks whether it should spawn a powerup (1 in 5 chance)
                if randint(1, powerup_chance) == 1:
                    # Makes sure that the powerup does not overlap the spike; can still occur but not as frequent
                    new_rect = pygame.Rect(WIDTH + 100, randint(75, HEIGHT - 75), 40, 40)
                    for spike in spikes:
                        if new_rect.colliderect(spike) == True:
                            new_rect.x += 100
                    screen_powerups.append(new_rect)

            # Triggered when the player clicks on a powerup
            # Makes sure that the player does not already have 3 powerups
            if event.type == GAIN_POWERUP and len(powerups) < 3:
                # Chooses a random powerup type
                powerup_type = choice(['thruster_speed', 'slow_down' , 'no_collision'])
                
                if powerup_type == 'thruster_speed':
                    powerups.append(Powerup(powerup_type, choice([120, 130, 140, 150, 160, 170]), THRUSTER_SPEED_POWERUP_IMG))

                if powerup_type == 'slow_down':
                    powerups.append(Powerup(powerup_type, choice([120, 130, 140, 150, 160, 170]), SLOW_DOWN_POWERUP_IMG))

                if powerup_type == 'no_collision':
                    powerups.append(Powerup(powerup_type, choice([40, 50, 60, 70, 80]), NO_COLLISION_POWERUP_IMG))

                if sound == True:
                    gameplay_channel.play(POWERUP_GAIN_SOUND)


                    
        # Player

        # Run the players functions
        player_movement()
        check_for_hit()

        # if current_state == 'moving' and prev_state == 'idle':
            # thruster_channel.play(THRUSTER_SOUND, -1)
        # else:
            # thruster_channel.stop()
        if current_state == 'moving' and thruster_channel.get_busy() == False:
            thruster_channel.play(THRUSTER_SOUND, -1)
        if current_state == 'idle':
            thruster_channel.stop()

        # Spikes
        # Increases the speed of the spikes scrolling past
        if next_scroll_speed_increase + 20 == score:
            next_scroll_speed_increase += 20
            scroll_vel += 1
            thruster_vel += 1

        if spawn_spike_timer >= 125:
            spawn_spike_timer = 0
            pygame.event.post(spawn_spike_event)
        spawn_spike_timer += 1

        # Remvoes any spikes that are off the edge of the screen to help with performance
        for spike in spikes:
            spike.rect.x -= scroll_vel
            if spike.rect.x <= -200:
                if spike.type == 'top':
                    score += 1
                spikes.remove(spike)

        # Score
        if score > highscore:
            highscore = score
            new_high_score = True
            save_data(highscore, music, sound)
            if shown_high_score_msg == False:
                high_score_msg_timer = 0
                shown_high_score_msg = True

        if new_high_score:
            if high_score_msg_timer >= 200:
                new_high_score = False
                show_high_score_msg = True
                shown_high_score_msg = True
            high_score_msg_timer += 1

                
        # Removes any powerups that are off the edge of the screen to help with performance
        for powerup in screen_powerups:
            powerup.x -= scroll_vel
            if powerup.x <= -200:
                screen_powerups.remove(powerup)

        # Background
        for obj in fg:
            obj.x -= scroll_vel
            if obj.x <= -500:
                obj.x = WIDTH
        for obj in mg:
            obj.x -= scroll_vel - 1
            if obj.x <= -500:
                obj.x = WIDTH
        for obj in bg:
            if using_powerup and current_powerup.type == 'slow_down' and next_scroll_speed_increase == 20:
                obj.x -= scroll_vel - 1
            else:   
                obj.x -= scroll_vel - 2
            if obj.x <= -500:
                obj.x = WIDTH
            
                
        # Updates the display
        # Draws the background image
        WIN.blit(STARS_BG_IMG, (0, 0))
        [WIN.blit(BG_IMG, obj) for obj in bg]
        [WIN.blit(MG_IMG, obj) for obj in mg]
        [WIN.blit(FG_IMG, obj) for obj in fg]
        WIN.blit(PLANET_IMG, (0, 0))

        # Draws each of the spikes
        [WIN.blit(spike.img, (spike.rect.x, spike.rect.y)) for spike in spikes]

        # Draws the collectable powerups on the screen, not the ones the player has
        [WIN.blit(POWERUP_IMG, powerup) for powerup in screen_powerups]

        # Gets the current frame for the player for the animation; may just be the regular image
        frame = pygame.transform.scale(
            other.get_frame(PLAYER_IMG, 20, 20, current_frame), (100, 100))
        # Draws the player image
        WIN.blit(frame, player)


        # Draws the bar of powerups that the player has
        WIN.blit(POWERUP_BAR_IMG, (WIDTH - 180 - 10, 10))
        
        # Try and excepts are nessescary in case the player does not have 3 powerups
        try:
            # Draws the player's first powerup on the powerup bar
            if powerups[0]:
                WIN.blit(powerups[0].img, ((WIDTH - 184), 15))
        except IndexError:
            pass
        try:
            # Draws the player's second powerup on the powerup bar
            if powerups[1]:
                WIN.blit(powerups[1].img, (WIDTH - 124, 15))
        except IndexError:
            pass
        try:
            # Draws the player's third powerup on the powerup bar
            if powerups[2]:
                WIN.blit(powerups[2].img, (WIDTH - 66, 15))
        except IndexError:
            pass

        # Handles the powerup timer to indicate how much time left the powerup has
        # Works by finding 10% of the current powerup duration and 10% of the powerup bar
        # When the powerup time reaches a percent that is a multiple of ten (10%, 20%, 30%)
        # It will run update the bar
        if using_powerup:
            # Draws the powerup timer bar image
            WIN.blit(POWERUP_TIMER_IMG, (WIDTH - 106, 90))

            # Finds 10% of the current powerup duration
            tnth_of_current_pwrup_duration = current_powerup.duration / 10

            # Runs until it finds how many percent of the bar needs to be filled
            finding_multiple_of_ten_pwrup = True
            x = 0
            while finding_multiple_of_ten_pwrup == True:
                x += 1
                # Makes sure that the bar actually increases
                if powerup_time >= tnth_of_current_pwrup_duration * x and x >= pwrup_tenth_of_bar_reached:
                    powerup_bar_time += 1
                    pwrup_tenth_of_bar_reached += 1
                    finding_multiple_of_ten_pwrup = False
                
                if x >= 20:
                    finding_multiple_of_ten_pwrup = False

            # Change the color of the powerup timer
            if powerup_bar_time == 0: powerup_timer_color = (0, 255, 0)
            if powerup_bar_time == 1: powerup_timer_color = (30, 255, 0)
            if powerup_bar_time == 2: powerup_timer_color = (75, 255, 0)
            if powerup_bar_time == 3: powerup_timer_color = (150, 255, 0)
            if powerup_bar_time == 4: powerup_timer_color = (225, 255, 0)
            if powerup_bar_time == 5: powerup_timer_color = (255, 225, 0)
            if powerup_bar_time == 6: powerup_timer_color = (255, 150, 0)
            if powerup_bar_time == 7: powerup_timer_color = (255, 75, 0)
            if powerup_bar_time == 8: powerup_timer_color = (255, 50, 0)
            if powerup_bar_time == 9: powerup_timer_color = (255, 25, 0)
            if powerup_bar_time == 10: powerup_timer_color = (255, 0, 0)
            
            # Fill up the powerup bar    
            pygame.draw.rect(WIN, powerup_timer_color, pygame.Rect(WIDTH - 103, 93, powerup_bar_time * 9, 24))

        # Show the player's score
        score_text = PRESSSTART2P_FONT.render(str(score), True, (200, 200, 220))
        WIN.blit(score_text, (10, 10))
        high_score_text = PRESSSTART2P_FONT_SMALL.render(f'Best:{highscore}', True, (200, 200, 220))
        WIN.blit(high_score_text, (10, 50))

        if new_high_score and show_high_score_msg and shown_high_score_msg == False:
            high_score_msg = PRESSSTART2P_FONT_MED.render('NEW HIGH SCORE!', True, (255, 0, 0))
            WIN.blit(high_score_msg, (10, HEIGHT - 50))

        # Pause button
        pause_button.process(events=events)

        WIN.blit(pause_button.display_img, pause_button.rect)
    
        pygame.display.update()



def get_prev_screen(bg, mg, fg, spikes, screen_powerups, current_frame, player):

    prev_screen = pygame.Surface((WIDTH, HEIGHT))
    
    prev_screen.blit(STARS_BG_IMG, (0, 0))
    prev_screen.blit(PLANET_IMG, (0, 0))
    [prev_screen.blit(BG_IMG, obj) for obj in bg]
    [prev_screen.blit(MG_IMG, obj) for obj in mg]
    [prev_screen.blit(FG_IMG, obj) for obj in fg]
    
    [prev_screen.blit(spike.img, (spike.rect.x, spike.rect.y)) for spike in spikes]
    [prev_screen.blit(POWERUP_IMG, powerup) for powerup in screen_powerups]
    
    frame = pygame.transform.scale(other.get_frame(PLAYER_IMG, 20, 20, current_frame), (100, 100))
    prev_screen.blit(frame, player)
    return prev_screen

def restart():
    main()

def pause_screen_main():
    global current_state
    crash_channel.pause()
    gameplay_channel.pause()
    thruster_channel.pause()
    menus.pause_screen(bg, mg, fg, spikes, screen_powerups, current_frame, player)

    
        

if __name__ == '__main__':
    pygame.mixer.music.play(-1)
    menus.title_screen()
    main()