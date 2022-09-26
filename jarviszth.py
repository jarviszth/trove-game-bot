import numpy as np
from pynput.keyboard import Key, Controller
import os, cv2, win32gui, win32ui, win32con, win32api, time, warnings, pygetwindow, random
warnings.simplefilter("ignore", DeprecationWarning)

title_game = 'Trove'
win = pygetwindow.getWindowsWithTitle(title_game)[0]
win.size = (1280, 768)
win.topleft = (0, 0)
hwnd = win32gui.FindWindow(None, title_game)
win_size = win32gui.GetWindowRect(hwnd)
keyboard = Controller()

lobby = True

x, y, w, h = 8, 30, win_size[2] - win_size[0], win_size[3] - win_size[1]
w = w - (x * 2)
h = h - (y + x)

def init():
    os.system('title JARVISZTH BOT')
    print("scan image plese wait...")

def click(x, y):
    try:win.activate()
    except: return
    else:
        time.sleep(.5)
        win32api.SetCursorPos((x, y))
        time.sleep(.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        # time.sleep(1)

def requeue():
    try:item = cv2.imread("img/requeue.png")
    except:return
    else:
        result = cv2.matchTemplate(screen, item, cv2.TM_SQDIFF_NORMED)
        loc_cut = np.where(result <= .03)
        loc_complete = list(zip(*loc_cut[::-1]))
        
        for loc in loc_complete:
            click(loc[0] + x, loc[1] + y)
            print("Requeue...")
            time.sleep(5)
            break
    
def disconnect():
    try:item = cv2.imread("img/error.png")
    except:return
    else:
        result = cv2.matchTemplate(screen, item, cv2.TM_SQDIFF_NORMED)
        loc_cut = np.where(result <= .03)
        loc_complete = list(zip(*loc_cut[::-1]))
        
        for loc in loc_complete:
            click(loc[0] + x, loc[1] + y)
            global lobby
            lobby = True
            print("Connect...")
            time.sleep(30)
            break

def AntiAFK():
    try:item = cv2.imread("img/people.png")
    except:return
    else:
        result = cv2.matchTemplate(screen, item, cv2.TM_SQDIFF_NORMED)
        loc_cut = np.where(result <= .03)
        loc_complete = list(zip(*loc_cut[::-1]))
        
        for loc in loc_complete:
            click(loc[0] + x, loc[1] + 300)
            print("Anti AFK...")
            time.sleep(random.randint(15,30))
            break

def joinBomb():
    try:item = cv2.imread("img/bomb.png")
    except:return
    else:
        result = cv2.matchTemplate(screen, item, cv2.TM_SQDIFF_NORMED)
        loc_cut = np.where(result <= .03)
        loc_complete = list(zip(*loc_cut[::-1]))
        
        for loc in loc_complete:
            try:win.activate()
            except:return
            else:
                time.sleep(.5)
                keyboard.press('b')
                time.sleep(.5)
                click(loc[0] + x, loc[1] + y)
                time.sleep(1)
                
                try:item = cv2.imread("img/yes.png")
                except:return
                else:
                    result = cv2.matchTemplate(screen, item, cv2.TM_SQDIFF_NORMED)
                    loc_cut = np.where(result <= .03)
                    loc_complete = list(zip(*loc_cut[::-1]))
                    
                    for loc in loc_complete:
                        click(loc[0] + x, loc[1] + y)
                        global lobby
                        lobby = False
                        print("Join Bomb...")
                        break
                time.sleep(3)


init()

while True:
    WDC = win32gui.GetWindowDC(hwnd)
    DCUI = win32ui.CreateDCFromHandle(WDC)
    CB = win32ui.CreateBitmap()
    CB.CreateCompatibleBitmap(DCUI, w, h)
    savescrenshot = DCUI.CreateCompatibleDC()
    savescrenshot.SelectObject(CB)
    savescrenshot.BitBlt((0, 0), (w, h), DCUI, (x, y), win32con.SRCCOPY)
    bitmaparray = CB.GetBitmapBits(True)
    screen = np.fromstring(bitmaparray, dtype = 'uint8')
    screen.shape = (h, w, 4)
    DCUI.DeleteDC()
    savescrenshot.DeleteDC()
    win32gui.ReleaseDC(hwnd, WDC)
    win32gui.DeleteObject(CB.GetHandle())
    screen = screen[...,:3]
    screen = np.ascontiguousarray(screen)
    
    disconnect()
    requeue()
    AntiAFK()
    if lobby:
        joinBomb()
        
    # cv2.imshow('JARVISZTH', screen)
    # if cv2.waitKey(1) == ord("q"):
    #     cv2.destroyAllWindows()
    #     break
    