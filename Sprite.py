import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class SpriteClass:
    #This is built to contain only one animation cycle. For multiple animation cycles of the same "character", use different objects
    def __init__(self, path_to_file):
        self.animated = False
        if "spritesheet" in path_to_file:
            self.animated = True
        self.spriteImage = cv2.imread(path_to_file, cv2.IMREAD_UNCHANGED)
        self._x = 0
        self._y = 0
        self._opacity = 1.0      # 1.0 = fully visible, 0.0 = invisible
        self._scale_x = 1.0      # 1.0 = original size
        self._scale_y = 1.0
        self._angle = 0          # degrees

    def setOpacity(self,opacity_):
        if 1>=opacity_>=0:
            self._opacity = opacity_
    def animate(self):
        pass
    def scale(self, x, y):
        self._scale_x = x
        self._scale_y = y
    def rotate(self,angle):
        self._angle = angle
    def setPosition(self,x_inp,y_inp):
        self._x = x_inp
        self._y = y_inp

    def _overlay(self, background, overlay, x, y):
        h, w = overlay.shape[:2]
        if x < 0 or y < 0 or x + w > background.shape[1] or y + h > background.shape[0]:
            return background  # skip drawing if it goes off-screen
        alpha = overlay[:, :, 3] / 255.0
        alpha = alpha[:, :, None]
        region = background[y:y+h, x:x+w]
        blended = (alpha * overlay[:, :, :3] + (1 - alpha) * region).astype("uint8")
        background[y:y+h, x:x+w] = blended
        return background        
    
    def draw(self, frame):
        img = self.spriteImage

        # 1. Apply scale
        h, w = img.shape[:2]
        new_w = max(1, int(w * self._scale_x))
        new_h = max(1, int(h * self._scale_y))
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # 2. Apply rotation
        if self._angle != 0:
            center = (new_w // 2, new_h // 2)
            matrix = cv2.getRotationMatrix2D(center, self._angle, 1.0)
            img = cv2.warpAffine(img, matrix, (new_w, new_h))

        # 3. Apply opacity (scale down the alpha channel)
        if self._opacity < 1.0:
            img = img.copy()
            img[:, :, 3] = (img[:, :, 3] * self._opacity).astype("uint8")

        # 4. Blend onto the frame at the sprite's position
        frame = self._overlay(frame, img, self._x, self._y)
        return frame
