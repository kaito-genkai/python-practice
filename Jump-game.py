from random import randint
import pyxel

class App:
    def __init__(self):
        pyxel.init(200, 120)
        pyxel.load("..\Jump Game\jump_game.pyxres")

        # スコア
        self.score = 0
        self.player_x = 72
        self.player_y = -16
        # Y方向の速度
        self.player_vy = 0
        self.player_is_alive = True
        # 遠い雲
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        # 近い雲
        self.near_cloud = [(10, 25), (70, 35), (200, 15)]
        # 床の配置
        self.floor = [(i * 60, randint(50, 104), True) for i in range(4)]
        # フルーツの配置
        self.fruit = [(i * 60, randint(0, 104), randint(0, 2), True) for i in range(4)]
        # BGMの再生(音でかいのでコメントアウト)
        #pyxel.playm(0, loop=True)
        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        # 床の更新
        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)

        # フルーツの更新
        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        # 左を押した場合
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, pyxel.width - 239)
        
        # 右を押した場合
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
        # 速度の分だけプレイヤーを動かす
        self.player_y += self.player_vy
        # Y方向の最大値(8)
        self.player_vy = min(self.player_vy + 1, 6)

        # プレイヤーのy座標が画面外にいったら
        if self.player_y > pyxel.height:
            if self.player_is_alive:
                self.player_is_alive = False
                pyxel.play(3, 5)
            
            if self.player_y > 600:
                self.score = 0
                self.player_x = 72
                self.player_y = -16
                self.player_vy = 0
                self.player_is_alive = True

    def update_floor(self, x, y, is_active):
        if is_active:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_vy > 0
            ):
                is_active = False
                self.score += 10
                self.player_vy = -12
                pyxel.play(3, 3)
        else:
            y += 6
        # 床を左に動かす
        x -= 4

        # 画面外に出た場合
        if x < - 40:
            # 画面右に移動
            x += 240
            y = randint(50, 104)
            is_active = True

        return x, y, is_active
    
    def update_fruit(self, x, y, kind, is_active):
        # フルーツとプレイヤーの当たり判定
        # absは絶対値。x,y座標ともにプレイヤーとフルーツの距離が12より小さくなったら
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_active = False
            # スコア加算
            self.score += (kind + 1) * 100
            # 最小-8のスピードで上に飛ぶ
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)
        # 左に動かす
        x -= 2

        # 画面外左に出たら
        if x < -40:
            # 画面外、右に移動
            x += 240
            y = randint(0, 104)
            kind = randint(0, 2)
            is_active = True

        return (x, y, kind, is_active)
    
    def draw(self): 
        # clear screen 画面をクリア
        pyxel.cls(12)
        # 空描画
        pyxel.blt(0, 88, 0, 0, 88, 160, 32)
        # 山描画
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)
        # 森描画
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)
        # 雲描画
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # 床描画
        for x, y, is_active in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        # フルーツ描画
        for x, y, kind, is_active in self.fruit:
            if is_active:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)

        # プレイヤー描画
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            16 if self.player_vy > 0 else 0,
            0,
            16,
            16,
            12,
        )

        # スコア描画
        s = "SCORE {:>4}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)
App()