import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image, ImageTk
import copy
import math
import pygame
import os
from PIL import Image, ImageTk, ImageFilter

class OthelloGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello")
        self.mode = None
        self.player_color = None
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.current_player = 'black'
        self.move_history = []
        self.last_move = None
        self.PHOTO_DIR = 'Photo'

        self.board_theme = 'green'
        self.piece_style = 'default'

        self.theme_colors = {
            'green': 'green', 'red': '#B22222', 'blue': '#4682B4', 'bvs': '#4A4A4A'
        }
        
        self.theme_photo_images = {}
        self.piece_photo_images = {}
        self.piece_images = {}
        self.board_bg_images = {}
        self.selected_theme_tag = None
        self.selected_piece_tag = None
        self.music_on = tk.BooleanVar(value=True)
        self.sfx_on = tk.BooleanVar(value=True)
        self.ai_depth = 3

        self.root.configure(bg="#2c3e50")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        pygame.mixer.init()
        try:
            pygame.mixer.music.load('Background_Music.mp3')
            pygame.mixer.music.play(-1)
            self.dice_roll_sound = pygame.mixer.Sound('Piece_Place.wav')
            # --- خط جدید: بارگذاری صدای خطا ---
            self.error_sound = pygame.mixer.Sound('Wrong_Placement.mp3')
        except Exception as e:
            print(f"Error loading sound: {e}")
            self.dice_roll_sound = None
            self.error_sound = None 
        
        self.load_theme_assets()
        self.load_game_assets()
        self.show_splash_screen()

    def _create_rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """A helper method to draw a rounded rectangle on a given canvas."""
        points = [x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
                x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
                x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def load_game_assets(self):
        """این تابع سایزبندی اصلی و متفاوت مهره‌ها را برمی‌گرداند و سایز هاور را هم محاسبه می‌کند"""
        piece_files = {
            'default': {'black': '4.png', 'white': '3.png'},
            'alt1': {'black': 'piece2.png', 'white': 'piece1.png'},
            'bvs': {'black': 'batman.png', 'white': 'superman.png'}
        }
        
        size_large = (45, 45)
        size_medium = (40, 40)
        size_small = (35, 35)
        hover_increase = 10  

        for style_name, files in piece_files.items():
            try:
                black_img_orig = Image.open(os.path.join(self.PHOTO_DIR, files['black'])).convert("RGBA")
                white_img_orig = Image.open(os.path.join(self.PHOTO_DIR, files['white'])).convert("RGBA")
                
                if style_name == 'alt1':
                    black_size, white_size = size_large, size_small
                elif style_name == 'default':
                    black_size, white_size = size_large, size_small
                elif style_name == 'bvs':
                    black_size, white_size = size_medium, size_large
                else:
                    black_size, white_size = size_large, size_large
                
                black_hover_size = (black_size[0] + hover_increase, black_size[1] + hover_increase)
                white_hover_size = (white_size[0] + hover_increase, white_size[1] + hover_increase)

                self.piece_images[style_name] = {
                    'black': {
                        'normal': ImageTk.PhotoImage(black_img_orig.resize(black_size, Image.LANCZOS)),
                        'large': ImageTk.PhotoImage(black_img_orig.resize(black_hover_size, Image.LANCZOS))
                    },
                    'white': {
                        'normal': ImageTk.PhotoImage(white_img_orig.resize(white_size, Image.LANCZOS)),
                        'large': ImageTk.PhotoImage(white_img_orig.resize(white_hover_size, Image.LANCZOS))
                    }
                }
            except FileNotFoundError:
                print(f"Warning: Game piece images not found for style '{style_name}'")

        try:
            bvs_bg_orig = Image.open(os.path.join(self.PHOTO_DIR, 'batmanvssuperman.jpg'))
            bvs_bg_resized = bvs_bg_orig.resize((400, 400), Image.LANCZOS)
            bvs_bg_blurred = bvs_bg_resized.filter(ImageFilter.GaussianBlur(3))
            self.board_bg_images['bvs'] = ImageTk.PhotoImage(bvs_bg_blurred)
        except FileNotFoundError:
            print("Warning: bvs theme background image not found.")
     
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_splash_screen(self):
        self.clear_frame()
        self.splash_frame = tk.Frame(self.root)
        self.splash_frame.pack()

        splash_image = Image.open(os.path.join(self.PHOTO_DIR, "Othello.jpg"))
        splash_image = splash_image.resize((600, 600), Image.LANCZOS)
        splash_photo = ImageTk.PhotoImage(splash_image)

        splash_label = tk.Label(self.splash_frame, image=splash_photo)
        splash_label.image = splash_photo  # Keep a reference
        splash_label.pack()


        # --- رفتن به منوی اصلی بعد از 6 ثانیه (6000 میلی‌ثانیه) ---
        self.root.after(2000, self.create_start_screen)

    def create_start_screen(self):
        self.clear_frame()
        canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        try:
            bg_image_pil = Image.open(os.path.join(self.PHOTO_DIR, "background.jpg"))
            bg_image_pil = bg_image_pil.resize((600, 600), Image.LANCZOS)
            blurred_image = bg_image_pil.filter(ImageFilter.GaussianBlur(10))
            self.bg_image = ImageTk.PhotoImage(blurred_image)
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except FileNotFoundError:
            canvas.configure(bg="#ECECEC")

        # The local definition is gone, and we now call the class method
        self._create_rounded_rect(canvas, 100, 40, 500, 560, radius=20, fill="white", stipple="gray50", outline="")

        title_font = ("Impact", 48, "bold")
        canvas.create_text(300, 100, text="OTHELLO", font=title_font, fill="#1c2833")

        self.menu_icons = {
            "one_player": ImageTk.PhotoImage(Image.open(os.path.join(self.PHOTO_DIR, "1.png")).resize((50, 50))),
            "two_players": ImageTk.PhotoImage(Image.open(os.path.join(self.PHOTO_DIR, "2.png")).resize((50, 50))),
            "options": ImageTk.PhotoImage(Image.open(os.path.join(self.PHOTO_DIR, "setting.png")).resize((50, 50))),
            "how_to_play": ImageTk.PhotoImage(Image.open(os.path.join(self.PHOTO_DIR, "q.png")).resize((50, 50))),
            "exit": ImageTk.PhotoImage(Image.open(os.path.join(self.PHOTO_DIR, "exit2.png")).resize((50, 50)))
        }

        button_font = ("Calibri", 20, "bold")
        initial_fg = "#2C3E50"
        hover_fg = "white"

        menu_items = [
            ("One Player", self.show_color_choice_screen, self.menu_icons["one_player"]),
            ("Two Players", self.start_two_player_mode, self.menu_icons["two_players"]),
            ("Options", self.opetions_mode, self.menu_icons["options"]),
            ("How To Play", self.how_to_play_mode, self.menu_icons["how_to_play"]),
            ("Exit", self.exit_mode, self.menu_icons["exit"])
        ]

        y_position = 180
        for text, command, icon in menu_items:
            tag = f"button_{text.replace(' ', '_')}"
            icon_x, text_x = 150, 220
            canvas.create_image(icon_x, y_position, image=icon, anchor="w", tags=(tag, f"{tag}_icon"))
            canvas.create_text(text_x, y_position, text=text, font=button_font, fill=initial_fg, anchor="w", tags=(tag, f"{tag}_text"))

            def on_enter(e, current_tag=tag):
                canvas.itemconfig(f"{current_tag}_text", fill=hover_fg)
            def on_leave(e, current_tag=tag):
                canvas.itemconfig(f"{current_tag}_text", fill=initial_fg)

            canvas.tag_bind(tag, "<Enter>", on_enter)
            canvas.tag_bind(tag, "<Leave>", on_leave)
            canvas.tag_bind(tag, "<Button-1>", lambda e, c=command: c())
            y_position += 70

        
    def draw_board(self):
        """این تابع حالا از سایز 'normal' مهره‌ها استفاده می‌کند"""
        self.canvas.delete("all")
        
        if self.board_theme == 'bvs' and self.board_bg_images.get('bvs'):
            self.canvas.create_image(0, 0, image=self.board_bg_images['bvs'], anchor="nw")
            grid_line_color = "#BBBBBB"
        else:
            board_color = self.theme_colors.get(self.board_theme, 'green')
            self.canvas.create_rectangle(0, 0, 400, 400, fill=board_color, outline="")
            grid_line_color = "black"

        for i in range(1, 8):
            self.canvas.create_line(i * 50, 0, i * 50, 400, fill=grid_line_color)
            self.canvas.create_line(0, i * 50, 400, i * 50, fill=grid_line_color)

        dot_color = grid_line_color
        dot_radius = 3
        dots_positions = [(100, 100), (100, 300), (300, 100), (300, 300)]
        for x, y in dots_positions:
            self.canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill=dot_color, outline="")

        current_pieces_data = self.piece_images.get(self.piece_style, self.piece_images.get('default'))
        if current_pieces_data:
            for r in range(8):
                for c in range(8):
                    piece_color = self.board[r][c]
                    if piece_color and current_pieces_data.get(piece_color):
                        # استفاده از سایز 'normal' برای نمایش در صفحه بازی
                        image_to_draw = current_pieces_data[piece_color]['normal']
                        self.canvas.create_image(c * 50 + 25, r * 50 + 25, image=image_to_draw)
        
        self.highlight_valid_moves()

    def load_theme_assets(self):
        """تابع برای بارگذاری تمام عکس‌های تم‌ها و مهره‌ها با مدیریت خطا"""
        # --- بارگذاری تم‌های صفحه ---
        themes = {'green': 'boardgreen.jpg', 'red': 'board red.jpg', 'blue': 'boardblue.png', 'bvs': 'batmanvssuperman.jpg'}
        for name, fname in themes.items():
            try:
                img = Image.open(os.path.join(self.PHOTO_DIR, fname))
                self.theme_photo_images[name] = {
                    'normal': ImageTk.PhotoImage(img.resize((60, 60))),
                    'large': ImageTk.PhotoImage(img.resize((80, 80)))
                }
            except FileNotFoundError:
                print(f"Warning: Theme image not found: {fname}")


        # --- بارگذاری تمام ست‌های مهره ---
        piece_styles = {
            'default': ('4.png', '3.png'),
            'alt1': ('piece2.png', 'piece1.png'),
            'bvs': ('batman.png', 'superman.png')
        }
        for name, files in piece_styles.items():
            try:
                f1, f2 = files
                # این خط برای اطمینان از اینکه همه عکس‌ها کانال آلفا دارند اضافه شده
                img1_orig = Image.open(os.path.join(self.PHOTO_DIR, f1)).convert("RGBA")
                img2_orig = Image.open(os.path.join(self.PHOTO_DIR, f2)).convert("RGBA")

                def create_combined(size):
                    spacing = 5  # فاصله بین دو مهره

                    def prepare_image(img, force_scale=False):
                        bbox = img.getbbox()
                        if bbox:
                            img = img.crop(bbox)

                        original_ratio = img.width / img.height
                        if original_ratio > 1:
                            new_width = size
                            new_height = int(size / original_ratio)
                        else:
                            new_height = size
                            new_width = int(size * original_ratio)

                        if force_scale:
                            scale_up = 1.35  # حالا دستی 35٪ بزرگتر می‌کنیم
                            new_width = int(new_width * scale_up)
                            new_height = int(new_height * scale_up)

                        img = img.resize((new_width, new_height), Image.LANCZOS)

                        background = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                        paste_x = (size - new_width) // 2
                        paste_y = (size - new_height) // 2
                        background.paste(img, (paste_x, paste_y), img)
                        return background

                    if name == "alt1":
                        img1_fixed = prepare_image(img1_orig.copy(), force_scale=True)   # piece2.png
                        img2_fixed = prepare_image(img2_orig.copy(), force_scale=False)  # piece1.png
                    else:
                        img1_fixed = prepare_image(img1_orig.copy())
                        img2_fixed = prepare_image(img2_orig.copy())

                    # اندازه‌ی تصویر نهایی با فاصله بین دو مهره
                    total_width = size * 2 + spacing
                    combined = Image.new('RGBA', (total_width, size), (0, 0, 0, 0))
                    combined.paste(img1_fixed, (0, 0))
                    combined.paste(img2_fixed, (size + spacing, 0))  # فاصله اضافه شد

                    return ImageTk.PhotoImage(combined)


                    # فقط برای alt1، piece2 رو بزرگ‌تر می‌کنیم (که دومیه‌ست)
                    if name == "alt1":
                        img1_fixed = prepare_image(img1_orig.copy(), force_scale=False)  # piece2.png
                        img2_fixed = prepare_image(img2_orig.copy(), force_scale=True)   # piece1.png
                    else:
                        img1_fixed = prepare_image(img1_orig.copy())
                        img2_fixed = prepare_image(img2_orig.copy())

                    combined = Image.new('RGBA', (size * 2, size), (0, 0, 0, 0))
                    combined.paste(img1_fixed, (0, 0))
                    combined.paste(img2_fixed, (size, 0))
                    return ImageTk.PhotoImage(combined)





                self.piece_photo_images[name] = {
                    'normal': create_combined(30), # سایز عادی
                    'large': create_combined(40)  # سایز بزرگ‌تر برای هاور
                }
            except FileNotFoundError:
                print(f"Warning: Piece images not found for style '{name}': {files}")


                
            
    def set_board_theme(self, theme_name):
        """تابع برای تغییر تم صفحه بازی"""
        self.board_theme = theme_name
        print(f"Board theme set to: {self.board_theme}")

    def set_piece_style(self, style_name):
        """تابع برای تغییر استایل مهره‌ها"""
        self.piece_style = style_name
        print(f"Piece style set to: {self.piece_style}")

        
    def opetions_mode(self):
        self.clear_frame()
        self.options_canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        self.options_canvas.pack(fill="both", expand=True)

        if hasattr(self, 'bg_image'):
            self.options_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            self.options_canvas.configure(bg="#2c3e50")

        self._create_rounded_rect(self.options_canvas, 50, 50, 550, 550, radius=20, fill="white", stipple="gray50", outline="")
        
        title_font = ("Impact", 36, "bold")
        self.options_canvas.create_text(300, 90, text="OPTIONS", font=title_font, fill="#1c2833")

        # نمایش تم‌ها و مهره‌ها
        self.render_themes()
        self.render_pieces()

        # بخش تنظیمات صدا
        self.options_canvas.create_text(100, 380, text="Sound Settings:", font=("Calibri", 16, "bold"), anchor="w")

        self.music_enabled = self.music_on.get()
        self.sfx_enabled = self.sfx_on.get()

        # --- تغییر اصلی: باکس و متن، خودشان قابل کلیک می‌شوند ---
        self.music_box = self._create_rounded_rect(
            self.options_canvas, 110, 421, 130, 441, radius=10, fill="", outline="black", width=2,
            tags="music_toggle"  # تگ کلیک به خود باکس اضافه شد
        )
        self.music_text = self.options_canvas.create_text(
            140, 431, text="Background Music", font=("Calibri", 14), anchor="w",
            tags="music_toggle"  # تگ کلیک به متن هم اضافه شد
        )
        self._draw_tick(self.music_box, self.music_enabled)

        self.sfx_box = self._create_rounded_rect(
            self.options_canvas, 110, 451, 130, 471, radius=10, fill="", outline="black", width=2,
            tags="sfx_toggle"  # تگ کلیک به خود باکس اضافه شد
        )
        self.sfx_text = self.options_canvas.create_text(
            140, 461, text="Move Sound Effects", font=("Calibri", 14), anchor="w",
            tags="sfx_toggle"  # تگ کلیک به متن هم اضافه شد
        )
        self._draw_tick(self.sfx_box, self.sfx_enabled)

        # رویدادها به همان تگ‌ها متصل باقی می‌مانند
        self.options_canvas.tag_bind("music_toggle", "<Button-1>", lambda e: self._toggle_music_box())
        self.options_canvas.tag_bind("sfx_toggle", "<Button-1>", lambda e: self._toggle_sfx_box())

        if hasattr(self, '_create_styled_button'):
            self._create_styled_button(self.options_canvas, 300, 510, "Back to Menu", self.create_start_screen)

    def _draw_tick(self, box_id, enabled):
        if hasattr(self, "_tick_lines"):
            for item in self._tick_lines.get(box_id, []):
                self.options_canvas.delete(item)
        else:
            self._tick_lines = {}

        if enabled:
            # --- تغییر اصلی فقط در این خط است ---
            # به جای "coords" از "bbox" استفاده می‌کنیم
            x1, y1, x2, y2 = self.options_canvas.bbox(box_id)
            
            tick1 = self.options_canvas.create_line(x1+3, (y1+y2)//2, (x1+x2)//2, y2-3, fill="#007BFF", width=2)
            tick2 = self.options_canvas.create_line((x1+x2)//2, y2-3, x2-3, y1+3, fill="#007BFF", width=2)
            self._tick_lines[box_id] = [tick1, tick2]
        else:
            self._tick_lines[box_id] = []



    def _toggle_music_box(self):
        self.music_enabled = not self.music_enabled
        self.music_on.set(self.music_enabled)
        self._draw_tick(self.music_box, self.music_enabled)
        self.toggle_music()  # قطع/وصل آهنگ

    def _toggle_sfx_box(self):
        self.sfx_enabled = not self.sfx_enabled
        self.sfx_on.set(self.sfx_enabled)
        self._draw_tick(self.sfx_box, self.sfx_enabled)


    def render_themes(self):
        self.options_canvas.create_text(100, 140, text="Board Theme:", font=("Calibri", 16, "bold"), anchor="w")
        x, y, padding = 130, 200, 110
        
        for name, images in self.theme_photo_images.items():
            tag = f"theme_{name}"
            self.options_canvas.create_image(x, y, image=images['normal'], tags=(tag,))
            self.options_canvas.tag_bind(tag, "<Enter>", lambda e, t=tag, n=name: self.on_item_enter(t, self.theme_photo_images[n]['large']))
            self.options_canvas.tag_bind(tag, "<Leave>", lambda e, t=tag, n=name: self.on_item_leave(t, self.theme_photo_images[n]['normal']))
            self.options_canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag, n=name: self.on_theme_click(t, n))
            x += padding
            
        self.selected_theme_tag = f"theme_{self.board_theme}"
        self.update_selection_indicator()

    # این نسخه را جایگزین تابع فعلی کنید
    # این کد را به طور کامل جایگزین تابع render_pieces فعلی خود کنید
    def render_pieces(self):
        self.options_canvas.create_text(100, 280, text="Piece Style:", font=("Calibri", 16, "bold"), anchor="w")
        x, y, padding = 150, 330, 140

        for name, images in self.piece_photo_images.items():
            tag = f"piece_{name}"
            img_combined = images['normal']
            self.options_canvas.create_image(x, y, image=img_combined, tags=(tag,))
            
            # --- اصلاح اصلی اینجاست ---
            # به جای توابع grow/shrink، از توابعی استفاده می‌کنیم که عکس را جایگزین می‌کنند
            # این کد دقیقا مثل بخش Board Theme عمل می‌کند
            self.options_canvas.tag_bind(tag, "<Enter>", lambda e, t=tag, n=name: self.on_item_enter(t, self.piece_photo_images[n]['large']))
            self.options_canvas.tag_bind(tag, "<Leave>", lambda e, t=tag, n=name: self.on_item_leave(t, self.piece_photo_images[n]['normal']))
            
            self.options_canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag, n=name: self.on_piece_click(t, n))
            x += padding
            
        self.selected_piece_tag = f"piece_{self.piece_style}"
        self.update_selection_indicator()

    def on_item_enter(self, tag, large_img):
        self.options_canvas.itemconfig(tag, image=large_img)
        self.options_canvas.tag_raise(tag)
        self.update_selection_indicator()

    def on_item_leave(self, tag, normal_img):
        self.options_canvas.itemconfig(tag, image=normal_img)
        self.update_selection_indicator()

        # این دو تابع جدید را به کلاس خود اضافه کنید
    def _on_canvas_item_grow(self, event):
        """تابع عمومی برای بزرگ کردن آیتم روی کانواس هنگام ورود موس"""
        widget = event.widget
        tag_tuple = widget.find_withtag(tk.CURRENT)
        if not tag_tuple: return
        tag = tag_tuple[0]

        coords = widget.bbox(tag)
        if coords:
            center_x = (coords[0] + coords[2]) / 2
            center_y = (coords[1] + coords[3]) / 2
            widget.scale(tag, center_x, center_y, 1.25, 1.25)
        widget.tag_raise(tag)

    def _on_canvas_item_shrink(self, event):
        """تابع عمومی برای کوچک کردن آیتم روی کانواس هنگام خروج موس"""
        widget = event.widget
        tag_tuple = widget.find_withtag(tk.CURRENT)
        if not tag_tuple: return
        tag = tag_tuple[0]

        coords = widget.bbox(tag)
        if coords:
            center_x = (coords[0] + coords[2]) / 2
            center_y = (coords[1] + coords[3]) / 2
            widget.scale(tag, center_x, center_y, 1/1.25, 1/1.25)

    def on_theme_click(self, tag, theme_name):
        self.board_theme = theme_name
        self.selected_theme_tag = tag
        self.update_selection_indicator()

    def on_piece_click(self, tag, piece_name):
        self.piece_style = piece_name
        self.selected_piece_tag = tag
        self.update_selection_indicator()

    def update_selection_indicator(self):
        self.options_canvas.delete("selection_border")
        
        tags_to_update = [self.selected_theme_tag, self.selected_piece_tag]

        for tag in tags_to_update:
            if tag and self.options_canvas.find_withtag(tag):
                coords = self.options_canvas.bbox(tag)
                if coords:
                    x1, y1, x2, y2 = coords
                    self._create_rounded_rect(
                        self.options_canvas, 
                        x1 - 6, y1 - 6, x2 + 6, y2 + 6,
                        radius=15,
                        fill="",  # --- این خط رو اضافه کن تا داخلش شفاف بشه ---
                        outline="#007BFF", 
                        width=4, 
                        tags="selection_border"
                    )
                



    def toggle_music(self):
        """قطع و وصل کردن موسیقی پس‌زمینه بر اساس چک‌باکس"""
        if self.music_on.get():
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()






    def opetions_mode_PlayGame(self):
        self.clear_frame()
        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack()

        sound_frame = tk.Frame(self.options_frame)
        sound_frame.pack(pady=10)

        tk.Label(sound_frame, text="Sound OF BackGround: ").pack(side=tk.LEFT)

        self.sound_button = tk.Button(sound_frame, text="Off", command=self.toggle_sound)
        self.sound_button.pack(side=tk.LEFT)

        # move_sound_frame = tk.Frame(self.options_frame)
        # move_sound_frame.pack(pady=10)

        # tk.Label(move_sound_frame, text="Move Sound: ").pack(side=tk.LEFT)

        # self.move_sound_button = tk.Button(move_sound_frame, text="Off", command=self.toggle_sound_Movement)
        # self.move_sound_button.pack(side=tk.LEFT)

        back_button = tk.Button(self.options_frame, text="Back", command=self.create_game_screen)
        back_button.pack(pady=10)

    # def toggle_sound_Movement(self):
    #     self.move_sound_enabled = not self.move_sound_enabled
    #     self.move_sound_button.config(text="On" if self.move_sound_enabled else "Off")
        
    def toggle_sound(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.sound_button.config(text="On")
        else:
            pygame.mixer.music.unpause()
            self.sound_button.config(text="Off")

    


    def _create_styled_button(self, canvas, x_pos, y_pos, text, command, width=85):
        """تابع کمکی برای ساخت دکمه‌های سفارشی با قابلیت تنظیم عرض"""
        
        font = ("Calibri", 16, "bold")
        initial_text_color = "#2C3E50"
        button_outline_color = "#2C3E50"
        initial_fill_color = "white"
        
        hover_fill_color = "#D5D8DC"
        hover_text_color = "white"

        tag = f"btn_{text.replace(' ', '')}"

            # --- تغییر اصلی اینجاست ---
        # به جای create_rectangle از تابع _create_rounded_rect برای کشیدن دکمه استفاده می‌کنیم
        x1, y1 = x_pos - width, y_pos - 22
        x2, y2 = x_pos + width, y_pos + 22
        radius = 20  # می‌تونی این مقدار رو برای گردی بیشتر یا کمتر تغییر بدی

        shape = self._create_rounded_rect(canvas, x1, y1, x2, y2, 
                                        radius=radius, 
                                        fill=initial_fill_color, 
                                        outline=button_outline_color,
                                        width=2,
                                        tags=(tag, f"{tag}_shape"))
        
        text_widget = canvas.create_text(x_pos, y_pos, text=text, font=font, 
                                        fill=initial_text_color, tags=(tag, f"{tag}_text"))


        def on_enter(event):
            canvas.itemconfig(shape, fill=hover_fill_color)
            canvas.itemconfig(text_widget, fill=hover_text_color)
        
        def on_leave(event):
            canvas.itemconfig(shape, fill=initial_fill_color)
            canvas.itemconfig(text_widget, fill=initial_text_color)

        canvas.tag_bind(tag, "<Enter>", on_enter)
        canvas.tag_bind(tag, "<Leave>", on_leave)
        canvas.tag_bind(tag, "<Button-1>", lambda e: command())


    



    def how_to_play_mode(self):
        self.clear_frame()
        canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        if hasattr(self, 'bg_image'):
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            canvas.configure(bg="#2c3e50")
        self._create_rounded_rect(canvas, 50, 50, 550, 550, radius=20, fill="white", stipple="gray50", outline="")


        title_font = ("Impact", 36, "bold")
        canvas.create_text(300, 100, text="HOW TO PLAY", font=title_font, fill="#1c2833")

        st = scrolledtext.ScrolledText(canvas, wrap=tk.WORD, bg="white", bd=1, relief="solid", font=("Calibri", 12))
        st.place(x=70, y=150, width=460, height=300)

        # --- متن کامل که به صورت یک متغیر جداگانه تعریف شده تا فاصله اضافی نداشته باشد ---
        instructions = ("Match Settings\n"
                        "Before starting a game, you will be presented with a Match Settings screen.\n"
                        "From here you can choose the side to play as (or alternating play as black and white) and the CPU difficulty (1 for beginners, and 10 for experts).\n\n"
                        "Playing Moves\n"
                        "Once a game has started, use the touch-screen or the dpad/joystick on the phone to select a legal square in which to place a piece.\n\n"
                        "Takeback\n"
                        "The Undo button can be used to take back as many moves as you want.\n\n"
                        "CPU Thinking\n"
                        "Player names and their scores are shown below the board.\n"
                        "When the CPU is thinking about a move, an animation will play in the center of the board.\n"
                        "Note that the higher the CPU difficulty, the longer the thinking times will be.\n\n"
                        "Menu\n"
                        "During play, you can press the phone's MENU button to get access to other features.\n"
                        "HINT will tell the CPU to assess your current situation and suggest a move.\n"
                        "SAVE & QUIT is always available under the MENU button - this will save any progress or settings changes you've made, and then exit.\n\n"
                        "Statistics\n"
                        "The game will track your wins/losses/draws and average score margins against each of the CPU levels.\n"
                        "This information can be accessed from the title menu screen, or from the Menu button during play.\n"
                        "The rating shown in the bottom left of the stats page is a cumulative rating calculated from all your games (This is not an ELO rating.)\n"
                        "Win percentage counts 1 point for win and 0.5 points for draw.\n\n"
                        )

        st.insert(tk.INSERT, instructions)
        st.config(state="disabled")

        # استفاده از دکمه‌های با استایل نهایی
        self._create_styled_button(canvas, 210, 500, "Game Rules", self.rules_mode)
        self._create_styled_button(canvas, 390, 500, "Return to Menu", self.create_start_screen)





    def rules_mode(self):
        self.clear_frame()
        canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        if hasattr(self, 'bg_image'):
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        else:
            canvas.configure(bg="#2c3e50")

        self._create_rounded_rect(canvas, 50, 50, 550, 550, radius=20, fill="white", stipple="gray50", outline="")


        title_font = ("Impact", 36, "bold")
        canvas.create_text(300, 100, text="GAME RULES", font=title_font, fill="#1C2833")

        st_bg_color = "white"
        st_fg_color = "black"
        st = scrolledtext.ScrolledText(canvas, wrap=tk.WORD, bg=st_bg_color, fg=st_fg_color,
                                    relief="solid", bd=1, font=("Calibri", 13))
        st.place(x=70, y=150, width=460, height=300)
        st.vbar.configure(troughcolor=st_bg_color, relief="flat", borderwidth=0)


        st.tag_configure('center', justify='center')

        # --- استفاده از متن و ترتیب کامل و دقیق کد قدیمی شما ---

        # 1. متن اول
        text1 = ("Reversi is a simple game played between two people on an 8 by 8 square board.\n"
                "The objective is to place pieces on the board so as to trap your opponent's pieces "
                "between your own and convert them to your own colour.\n\n"# --- متن اضافه شده ---
                "Each piece is black on one side and white on the other, with one colour assigned to each player. "
                "The game begins with two pieces of each colour on the board and the players must take it in turns "
                "to then try and capture their opponent's pieces. The player can only play on squares that allow a "
                "capture to occur. In the position below black can play 1 of 5 possible moves marked by the green dots. "
                "If they play on the square marked by the black circle, this will trap 2 white pieces (see below).\n\n")
        st.insert(tk.END, text1)

        # 2. عکس اول
        try:
            # استفاده از مسیر نسبی برای سازگاری بهتر
            rules_image1 = Image.open(os.path.join(self.PHOTO_DIR, "rules1.jpg")).resize((250, 150), Image.LANCZOS)
            self.rules_photo1 = ImageTk.PhotoImage(rules_image1)
            st.image_create(tk.END, image=self.rules_photo1)
            st.tag_add('center', 'end-2c linestart', 'end-2c lineend')
            st.insert(tk.END, "\n")
        except (FileNotFoundError, AttributeError):
            st.insert(tk.END, "\n[Image 'rules1.jpg' not found]\n")
        
        text3 = ("\nAfter playing this move the new position will be as follows, with one added new black piece "
                "and 2 white pieces converted to black pieces.\n")
        st.insert(tk.END, text3)
        # 4. عکس دوم
        try:
            rules_image2 = Image.open(os.path.join(self.PHOTO_DIR, "rules2.jpg")).resize((250, 150), Image.LANCZOS)
            self.rules_photo2 = ImageTk.PhotoImage(rules_image2)
            st.image_create(tk.END, image=self.rules_photo2)
            st.tag_add('center', 'end-2c linestart', 'end-2c lineend')
            st.insert(tk.END, "\n")
        except (FileNotFoundError, AttributeError):
            st.insert(tk.END, "\n[Image 'rules2.jpg' not found]\n")

        # 3. متن دوم
        text2 = ("\nIn this new position white only has one capture (shown above) which will capture 2 black pieces.\n"
                "If there is nowhere a player can place a piece that will trap and flip any of the opponent's pieces, "
                "the turn counts as a pass.\n"
                "Once there are no more legal moves left, the player with the most number of pieces showing their "
                "colour is the winner.\n\n")
        st.insert(tk.END, text2)

        

        st.config(state="disabled")

        # استفاده از دکمه با استایل نهایی
        self._create_styled_button(canvas, 300, 500, "Back", self.how_to_play_mode)

    
    def _confirm_return_to_menu(self):
        # سوال پرسیده می‌شود و اگر پاسخ "Yes" بود، به منوی اصلی برمی‌گردد
        if messagebox.askyesno("Return to Menu", "Are you sure you want to end this game?"):
            self.create_start_screen()

    def exit_mode(self):
        self._create_exit_screen()


    def _create_exit_screen(self):
        self.clear_frame()
        canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        if hasattr(self, 'bg_image'): canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # The local definition is gone, and we now call the class method
        self._create_rounded_rect(canvas, 100, 200, 500, 400, radius=20, fill="white", stipple="gray50", outline="")
        
        canvas.create_text(300, 250, text="Are you sure you want to exit?", font=("Calibri", 20, "bold"), fill="#1c2833")

        self._create_styled_button(canvas, 215, 330, "Yes", self.root.quit, width=80)
        self._create_styled_button(canvas, 385, 330, "No", self.create_start_screen, width=80)

    

    def _update_choice_screen_borders(self, canvas):
        canvas.delete("selection_border")
        
        tags_to_update = []
        if self.player_color:
            tags_to_update.append(f"piece_choice_{self.player_color}")
        
        if hasattr(self, 'selected_difficulty_tag'):
            tags_to_update.append(self.selected_difficulty_tag)

        for tag in tags_to_update:
            if canvas.find_withtag(tag):
                coords = canvas.bbox(tag)
                if coords:
                    x1, y1, x2, y2 = coords
                    self._create_rounded_rect(
                        canvas, 
                        x1 - 8, y1 - 8, x2 + 8, y2 + 8,
                        radius=20,
                        fill="",  # --- این خط رو هم اینجا اضافه کن ---
                        outline="#007BFF", 
                        width=3, 
                        tags="selection_border"
                    )



        # این تابع را به طور کامل با نسخه فعلی در کد خود جایگزین کنید
        # این نسخه را هم جایگزین تابع فعلی کنید
        # Find this function in your code and replace it completely with this version
    def show_color_choice_screen(self):
        """این تابع حالا با تعویض عکس، افکت بزرگنمایی را ایجاد می‌کند"""
        self.clear_frame()
        self.player_color = None
        self.ai_depth = 3
        self.selected_difficulty_tag = "diff_tag_0"
        self.choice_canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        self.choice_canvas.pack(fill="both", expand=True)

        if hasattr(self, 'bg_image'):
            self.choice_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # توابع کمکی برای هاور
        def on_piece_enter(event, piece_color):
            tag = f"piece_choice_{piece_color}"
            large_image = self.piece_images[self.piece_style][piece_color]['large']
            self.choice_canvas.itemconfig(tag, image=large_image)
            self.choice_canvas.tag_raise(tag)

        def on_piece_leave(event, piece_color):
            tag = f"piece_choice_{piece_color}"
            normal_image = self.piece_images[self.piece_style][piece_color]['normal']
            self.choice_canvas.itemconfig(tag, image=normal_image)
            self._update_choice_screen_borders(self.choice_canvas)
        
        def on_text_enter(event):
            tag = event.widget.find_withtag(tk.CURRENT)[0]
            event.widget.itemconfig(tag, font=("Calibri", 20, "bold"))

        def on_text_leave(event):
            tag = event.widget.find_withtag(tk.CURRENT)[0]
            event.widget.itemconfig(tag, font=("Calibri", 16, "bold"))

        self._create_rounded_rect(self.choice_canvas, 100, 80, 500, 520, radius=20, fill="white", stipple="gray50", outline="")
        self.choice_canvas.create_text(300, 130, text="Choose Your Piece", font=("Calibri", 18, "bold"), fill="#1c2833")
        
        style_images = self.piece_images.get(self.piece_style, self.piece_images.get('default', {}))
        
        def set_player_and_draw_border(color):
            self.player_color = color
            self.choice_canvas.itemconfig(self.error_text_id, state='hidden')
            self._update_choice_screen_borders(self.choice_canvas)

        if style_images:
            if style_images.get('black'):
                self.choice_canvas.create_image(230, 200, image=style_images['black']['normal'], tags="piece_choice_black")
                self.choice_canvas.tag_bind("piece_choice_black", "<Button-1>", lambda e: set_player_and_draw_border('black'))
                self.choice_canvas.tag_bind("piece_choice_black", "<Enter>", lambda e: on_piece_enter(e, 'black'))
                self.choice_canvas.tag_bind("piece_choice_black", "<Leave>", lambda e: on_piece_leave(e, 'black'))
            if style_images.get('white'):
                self.choice_canvas.create_image(370, 200, image=style_images['white']['normal'], tags="piece_choice_white")
                self.choice_canvas.tag_bind("piece_choice_white", "<Button-1>", lambda e: set_player_and_draw_border('white'))
                self.choice_canvas.tag_bind("piece_choice_white", "<Enter>", lambda e: on_piece_enter(e, 'white'))
                self.choice_canvas.tag_bind("piece_choice_white", "<Leave>", lambda e: on_piece_leave(e, 'white'))

        self.choice_canvas.create_text(300, 280, text="Select Difficulty", font=("Calibri", 18, "bold"), fill="#1c2833")
        difficulty_options = {"Easy": 3, "Normal": 5, "Hard": 7}
        def on_difficulty_click(tag, depth): self.ai_depth = depth; self.selected_difficulty_tag = tag; self._update_choice_screen_borders(self.choice_canvas)
        x_pos = 180
        for i, (text, depth) in enumerate(difficulty_options.items()):
            tag = f"diff_tag_{i}"
            self.choice_canvas.create_text(x_pos, 340, text=text, font=("Calibri", 16, "bold"), fill="#2C3E50", tags=(tag,))
            self.choice_canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag, d=depth: on_difficulty_click(t, d))
            self.choice_canvas.tag_bind(tag, "<Enter>", on_text_enter)
            self.choice_canvas.tag_bind(tag, "<Leave>", on_text_leave)
            x_pos += 120
            
        self._update_choice_screen_borders(self.choice_canvas)
        self.error_text_id = self.choice_canvas.create_text(300, 385, text="Please select a piece!", font=("Calibri", 14, "bold"), fill="red", state='hidden')
        self._create_styled_button(self.choice_canvas, 215, 450, "Start Game", self.confirm_start_one_player, width=80)
        self._create_styled_button(self.choice_canvas, 385, 450, "Back to Menu", self.create_start_screen, width=80)
        

    def start_two_player_mode(self):
        self.start_game("two_players")

    def set_player_color(self, color):
        self.player_color = color

    def confirm_start_one_player(self):
        if not self.player_color:
            # --- تغییر اصلی: به جای پاپ‌آپ، متن خطا نمایش داده می‌شود ---
            # messagebox.showwarning("Warning", "Please choose your piece!") (این خط حذف شد)
            self.choice_canvas.itemconfig(self.error_text_id, state='normal')
            return
        
        self.start_game("one_player")

    

    def start_game(self, mode):
        self.mode = mode
        self.setup_board_state() # <--- اینجا اصلاح شد
        self.create_game_screen()
        if self.mode == "one_player" and self.current_player != self.player_color:
            self.root.after(500, self.ai_move)

    def start_one_player_mode(self, color):
        self.mode = "one_player"
        self.player_color = color
        self.current_player = 'black'
        self.setup_board()
        self.create_game_screen()
        if self.player_color == 'white':
            self.root.after(500, self.ai_move)


    def setup_board_state(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.board[3][3], self.board[4][4] = 'white', 'white'
        self.board[3][4], self.board[4][3] = 'black', 'black'
        self.current_player = 'black'
        self.move_history = []

    def create_game_screen(self):
        self.clear_frame()
        
        main_canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        main_canvas.pack(fill="both", expand=True)
        
        if hasattr(self, 'bg_image'):
            main_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # The local definition is gone, and we now call the class method
        self._create_rounded_rect(main_canvas, 80, 30, 520, 570, radius=20, fill="white", stipple="gray50", outline="")
        
        self.status_label_id = main_canvas.create_text(300, 55, text="", font=("Calibri", 16, "bold"), fill="#1c2833")

        self.canvas = tk.Canvas(main_canvas, width=400, height=400, borderwidth=0, highlightthickness=0)
        main_canvas.create_window(300, 270, window=self.canvas)
        self.canvas.bind("<Button-1>", self.click_handler)
        
        self.score_label_id = main_canvas.create_text(300, 490, text="", font=("Calibri", 16, "bold"), fill="#1c2833")
        
        self.main_canvas = main_canvas

        self._create_styled_button(main_canvas, 225, 535, "Undo", self.undo_move, width=65)
        self._create_styled_button(main_canvas, 375, 535, "Menu", self.create_start_screen, width=65)

        self.draw_board()
        self.update_score_and_status()

    

    def update_score_and_status(self):
        """تابع یکپارچه برای آپدیت امتیاز و وضعیت با نام‌های صحیح"""
        name_map = {"black": "Black", "white": "White"}
        
        # --- تغییر اصلی اینجاست: اضافه شدن شرط برای استایل alt1 ---
        if self.piece_style == "bvs":
            name_map = {"black": "Batman", "white": "Superman"}
        elif self.piece_style == "alt1":
            # بر اساس فایل‌های عکس: piece2.png مهره سیاه و piece1.png مهره سفید است
            name_map = {"black": "Sapphire", "white": "Ruby"}

        # محاسبه امتیازات
        black_score = sum(row.count('black') for row in self.board)
        white_score = sum(row.count('white') for row in self.board)
        
        # استفاده از نام‌های صحیح در متن امتیاز
        score_text = f"{name_map['black']}: {black_score}  |  {name_map['white']}: {white_score}"
        
        # استفاده از نام صحیح در متن نوبت
        player_name = name_map.get(self.current_player, self.current_player.capitalize())
        status_text = f"{player_name}'s Turn"

        # آپدیت متن‌ها روی Canvas اصلی
        if hasattr(self, 'main_canvas'):
            self.main_canvas.itemconfig(self.status_label_id, text=status_text)
            self.main_canvas.itemconfig(self.score_label_id, text=score_text)


    def handle_board_click(self, event):
        row = event.y // 50
        col = event.x // 50

        if self.is_valid_move(row, col, self.current_player):
            self.make_move(row, col, self.current_player)
            self.play_dice_roll_sound()  # Play sound on valid move
            self.update_board_ui()
            self.switch_player()

    def play_dice_roll_sound(self):
        if self.sfx_on.get(): # فقط در صورتی که تیک خورده باشد، صدا پخش می‌شود
            self.dice_roll_sound.play()
    

    
    def highlight_valid_moves(self):
        # اگر حالت تک‌نفره است و نوبت کامپیوتر، هایلایت نشان نده
        if self.mode == 'one_player' and self.current_player != self.player_color:
            return
             
        # تمام خانه‌های صفحه را بررسی کن
        for r in range(8):
            for c in range(8):
                # اگر حرکت در خانه‌ای مجاز بود، یک دایره زرد دور آن بکش
                if self.is_valid_move(self.board, r, c, self.current_player):
                    self.canvas.create_oval(c * 50 + 15, r * 50 + 15, c * 50 + 35, r * 50 + 35,
                                            outline="yellow", width=2)

    
    
    

    def apply_sim_move(self, board, move, player):
        """یک حرکت را روی یک صفحه کپی شده شبیه‌سازی می‌کند و نتیجه را برمی‌گرداند"""
        new_board = copy.deepcopy(board)
        row, col = move
        new_board[row][col] = player
        # از همان منطق اصلی بازی برای پیدا کردن مهره‌های قابل برگشت استفاده می‌کند
        pieces_to_flip = self.get_pieces_to_flip(new_board, row, col, player)
        for r, c in pieces_to_flip:
            new_board[r][c] = player
        return new_board
    
    
    def undo_move(self):
        if not self.move_history:
            return

        # در حالت تک‌نفره، اگر نوبت بازیکن باشد، دو حرکت به عقب برمی‌گردیم
        if self.mode == 'one_player' and self.current_player == self.player_color and len(self.move_history) >= 2:
            self.move_history.pop() # حرکت کامپیوتر را نادیده می‌گیریم
        
        # بازگشت به وضعیت قبلی
        last_board, last_player = self.move_history.pop()
        self.board = last_board
        self.current_player = last_player
        
        self.draw_board()
        self.update_score_and_status()
    

    def is_valid_move(self, board, row, col, player):
        if not (0 <= row < 8 and 0 <= col < 8 and board[row][col] == ''):
            return False
        # برای معتبر بودن یک حرکت، باید حداقل یک مهره حریف را برگرداند
        return len(self.get_pieces_to_flip(board, row, col, player)) > 0
    
    def get_pieces_to_flip(self, board, row, col, player):
        opponent = 'white' if player == 'black' else 'black'
        pieces_to_flip = []
        # بررسی هر هشت جهت اطراف مهره
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            line, r, c = [], row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                line.append((r, c))
                r, c = r + dr, c + dc
            # اگر در انتهای یک خط از مهره‌های حریف، مهره خودی پیدا شد، آن خط معتبر است
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                pieces_to_flip.extend(line)
        return pieces_to_flip

    def has_any_valid_move(self, board, player):
        # بررسی وجود حداقل یک حرکت معتبر برای بازیکن
        return any(self.is_valid_move(board, r, c, player) for r in range(8) for c in range(8))
    


    def flip_pieces(self, row, col, player):
        opponent = 'white' if player == 'black' else 'black'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            pieces_to_flip = []
            x, y = row + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == opponent:
                pieces_to_flip.append((x, y))
                x += dx
                y += dy
            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] == player:
                for px, py in pieces_to_flip:
                    self.board[px][py] = player

    def has_valid_move(self):
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col, self.current_player):
                    return True
        return False

    def _create_end_game_screen(self, winner_text, score1_text, score2_text):
        self.clear_frame()
        canvas = tk.Canvas(self.root, width=600, height=600, borderwidth=0, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        if hasattr(self, 'bg_image'): canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        def create_rounded_rect(x1, y1, x2, y2, radius, **kwargs):
            points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y2-radius, x2, y2, 
                      x2-radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
            return canvas.create_polygon(points, **kwargs, smooth=True)

        create_rounded_rect(100, 150, 500, 450, radius=20, fill="white", stipple="gray50", outline="")
        
        canvas.create_text(300, 200, text="GAME OVER", font=("Impact", 32, "bold"), fill="#1c2833")
        canvas.create_text(300, 250, text=winner_text, font=("Calibri", 22, "bold"), fill="#007BFF")
        canvas.create_text(300, 300, text=f"{score1_text} | {score2_text}", font=("Calibri", 18), fill="#1c2833")

        # --- تغییر اصلی: فاصله افقی دکمه‌ها از هم بیشتر شد ---
        self._create_styled_button(canvas, 215, 380, "Play Again", self.play_again, width=80)
        self._create_styled_button(canvas, 385, 380, "Return to Menu", self.create_start_screen, width=80)
    
    def end_game(self):
        black_score = sum(row.count('black') for row in self.board)
        white_score = sum(row.count('white') for row in self.board)
        
        name_map = {"black": "Black", "white": "White"}
        if self.piece_style == "bvs": name_map = {"black": "Batman", "white": "Superman"}
        elif self.piece_style == "alt1": name_map = {"black": "Sapphire", "white": "Ruby"}

        winner_color = None
        if black_score > white_score: winner_color = 'black'
        elif white_score > black_score: winner_color = 'white'

        winner_name = name_map.get(winner_color, "Nobody") if winner_color else "Nobody"
        final_text = f"{winner_name} Wins!" if winner_color else "It's a Draw!"

        # فراخوانی تابع جدید برای ساخت صفحه پایان بازی
        self._create_end_game_screen(final_text, f"{name_map['black']}: {black_score}", f"{name_map['white']}: {white_score}")

    
    

    def finish_program(self):
        self.root.quit()

    def return_to_menu(self):
        self.end_frame.destroy()
        self.setup_board()
        self.create_start_screen()

    def play_again(self):
        # نسخه جدید که دیگر باعث ارور نمی‌شود
        self.clear_frame()
        self.start_game(self.mode)

    
        # این تابع جدید را به کلاس خود اضافه کنید
    def flash_square(self, row, col, color="red", duration=250):
        """یک خانه را برای مدت کوتاهی به رنگ مشخصی درمی‌آورد."""
        # بررسی اینکه کلیک داخل محدوده برد باشد
        if not (0 <= row < 8 and 0 <= col < 8):
            return
            
        x1 = col * 50
        y1 = row * 50
        x2 = x1 + 50
        y2 = y1 + 50
        
        # یک مستطیل قرمز نیمه‌شفاف روی خانه می‌کشد
        flash_rect = self.canvas.create_rectangle(
            x1, y1, x2, y2, 
            fill="#363636", 
            outline="", 
            stipple="gray50", # این خاصیت حالت نیمه‌شفاف می‌دهد
            tags="flash_effect"
        )
        
        # پس از 250 میلی‌ثانیه، مستطیل را پاک می‌کند
        self.canvas.after(duration, lambda: self.canvas.delete(flash_rect))

    # این دو تابع جدید را به کلاس اضافه کنید

    # این دو تابع را جایگزین نسخه‌های قبلی کنید

    def _on_item_grow(self, event):
        """این تابع آیتم (عکس یا متن) را هنگام ورود موس بزرگ می‌کند"""
        # تصحیح شد: به جای self.root از self.choice_canvas استفاده می‌کنیم
        tag_tuple = self.choice_canvas.find_withtag(tk.CURRENT)
        if not tag_tuple: return # اگر تگی پیدا نشد، خارج شو
        tag = tag_tuple[0]

        # برای متن، فونت را بزرگ می‌کنیم
        if "text" in self.choice_canvas.itemcget(tag, "tags"):
            self.choice_canvas.itemconfig(tag, font=("Calibri", 19, "bold"))
        # برای عکس، آن را بزرگ‌تر می‌کنیم
        else:
            coords = self.choice_canvas.bbox(tag)
            if coords:
                center_x = (coords[0] + coords[2]) / 2
                center_y = (coords[1] + coords[3]) / 2
                self.choice_canvas.scale(tag, center_x, center_y, 1.15, 1.15)
        
        self.choice_canvas.tag_raise(tag)

    def _on_item_shrink(self, event):
        """این تابع آیتم را هنگام خروج موس به حالت اول برمی‌گرداند"""
        # تصحیح شد: به جای self.root از self.choice_canvas استفاده می‌کنیم
        tag_tuple = self.choice_canvas.find_withtag(tk.CURRENT)
        if not tag_tuple: return # اگر تگی پیدا نشد، خارج شو
        tag = tag_tuple[0]
        
        # برای متن، فونت را به حالت اول برمی‌گردانیم
        if "text" in self.choice_canvas.itemcget(tag, "tags"):
            self.choice_canvas.itemconfig(tag, font=("Calibri", 16, "bold"))
        # برای عکس، آن را کوچک‌تر می‌کنیم
        else:
            coords = self.choice_canvas.bbox(tag)
            if coords:
                center_x = (coords[0] + coords[2]) / 2
                center_y = (coords[1] + coords[3]) / 2
                self.choice_canvas.scale(tag, center_x, center_y, 1/1.15, 1/1.15)


    # این نسخه را جایگزین تابع فعلی کنید
    def click_handler(self, event):
        if self.mode == 'one_player' and self.current_player != self.player_color:
            return

        col, row = event.x // 50, event.y // 50
        
        # اگر حرکت معتبر بود
        if self.make_move(row, col):
            if self.mode == 'one_player' and self.current_player != self.player_color:
                self.root.after(500, self.ai_move)
        # --- بخش جدید: اگر حرکت نامعتبر بود ---
        else:
            # اگر صدای افکت فعال بود، صدای خطا پخش کن
            if self.sfx_on.get() and self.error_sound:
                self.error_sound.play()
            # در غیر این صورت، خانه را قرمز کن
            else:
                self.flash_square(row, col)

        # این نسخه را جایگزین تابع فعلی کنید
        # این نسخه را جایگزین تابع make_move فعلی کنید
    def make_move(self, row, col):
        if not self.is_valid_move(self.board, row, col, self.current_player):
            return False
        
        self.move_history.append((copy.deepcopy(self.board), self.current_player))
        
        pieces_to_flip = self.get_pieces_to_flip(self.board, row, col, self.current_player)
        self.board[row][col] = self.current_player
        for r, c in pieces_to_flip:
            self.board[r][c] = self.current_player
        
        if self.sfx_on.get() and self.dice_roll_sound:
            self.dice_roll_sound.play()
        
        self.current_player = 'white' if self.current_player == 'black' else 'black'
        
        if not self.has_any_valid_move(self.board, self.current_player):
            opponent = 'white' if self.current_player == 'black' else 'black'
            if not self.has_any_valid_move(self.board, opponent):
                self.draw_board()
                self.update_score_and_status()
                self.end_game()
                return False
            else:
                self.current_player = opponent
        
        self.draw_board()
        self.update_score_and_status()
        return True
    
    def ai_move(self):
        if self.current_player != self.player_color:
            # فراخوانی مینی‌مکس برای پیدا کردن بهترین حرکت
            _, move = self.minimax(self.board, self.ai_depth, -math.inf, math.inf, True, self.current_player)
            if move:
                # حرکت هوش مصنوعی انجام می‌شود
                self.make_move(move[0], move[1])
                
                # --- بخش کلیدی اضافه شده ---
                # پس از حرکت، بررسی کن که آیا نوبت بازیکن انسان رد شده و دوباره نوبت هوش مصنوعی است یا خیر.
                # اگر چنین بود، تابع را دوباره فراخوانی کن تا هوش مصنوعی به بازی ادامه دهد.
                if self.mode == 'one_player' and self.current_player != self.player_color:
                    self.root.after(500, self.ai_move)

    def minimax(self, board, depth, alpha, beta, maximizing, player):
        opponent = 'white' if player == 'black' else 'black'
        ai_color = 'white' if self.player_color == 'black' else 'black'

        if depth == 0 or not self.has_any_valid_move(board, player):
            return self.evaluate_board(board, ai_color), None
        
        valid_moves = [(r, c) for r in range(8) for c in range(8) if self.is_valid_move(board, r, c, player)]

        if not valid_moves:
            return self.evaluate_board(board, ai_color), None

        best_move = valid_moves[0]
        if maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                new_board = self.apply_sim_move(board, move, player)
                evaluation, _ = self.minimax(new_board, depth - 1, alpha, beta, False, opponent)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else: # Minimizing
            min_eval = math.inf
            for move in valid_moves:
                new_board = self.apply_sim_move(board, move, player)
                evaluation, _ = self.minimax(new_board, depth - 1, alpha, beta, True, opponent)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move
            
    def evaluate_board(self, board, ai_color):
        player_color = 'white' if ai_color == 'black' else 'black'
        return sum(row.count(ai_color) for row in board) - sum(row.count(player_color) for row in board)
   

    def get_valid_moves(self, board, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move_for_board(board, row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move_for_board(self, board, row, col, player):
        if board[row][col] != '':
            return False
        opponent = 'white' if player == 'black' else 'black'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            x, y = row + dx, col + dy
            if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == opponent:
                while 0 <= x < 8 and 0 <= y < 8:
                    x += dx
                    y += dy
                    if not (0 <= x < 8 and 0 <= y < 8):
                        break
                    if board[x][y] == player:
                        return True
                    if board[x][y] == '':
                        break
        return False

    def apply_move(self, board, move, player):
        new_board = copy.deepcopy(board)
        row, col = move
        new_board[row][col] = player
        self.flip_pieces_for_board(new_board, row, col, player)
        return new_board

    def flip_pieces_for_board(self, board, row, col, player):
        opponent = 'white' if player == 'black' else 'black'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in directions:
            pieces_to_flip = []
            x, y = row + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8 and board[x][y] == opponent:
                pieces_to_flip.append((x, y))
                x += dx
                y += dy
            if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == player:
                for px, py in pieces_to_flip:
                    board[px][py] = player

if __name__ == "__main__":
    root = tk.Tk()
    game = OthelloGame(root)
    root.mainloop()