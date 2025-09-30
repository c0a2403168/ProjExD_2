import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),    
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバーを表示する
    画面中央に「GAME OVER」と表示する
    五秒間表示した後、プログラムを終了する
    """
    gameover_sfc = pg.Surface((WIDTH, HEIGHT)) #からのSurfaceを作成する
    gameover_sfc.fill((0, 0, 0)) # 黒色で塗りつぶす
    gameover_sfc.set_alpha(150) # 透明度を設定する
    screen.blit(gameover_sfc, (0, 0)) # 画面に貼り付ける 
    font = pg.font.Font(None, 100) # フォントのサイズ決め
    text = font.render("GAME OVER", True, (255, 255, 255)) # ゲームオーバーを白色で表示
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) # 画面中央に表示
    screen.blit(text, text_rect)
    gameover_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0) # 泣いたこうかとんの画像
    gameover_kk_rect_1 = gameover_kk_img.get_rect(center=(WIDTH // 2 -300, HEIGHT // 2 )) # 画面左に表示
    gameover_kk_rect_2 = gameover_kk_img.get_rect(center=(WIDTH // 2 +300, HEIGHT // 2 )) # 画面右に表示
    screen.blit(gameover_kk_img, gameover_kk_rect_1)
    screen.blit(gameover_kk_img, gameover_kk_rect_2)
    pg.display.update() # 画面を更新する    
    time.sleep(5) # 5秒間表示する


    
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向、縦方向のはみ出し判定結果のタプル
    画面内ならtrue、画面外ならFalse   
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: # 横方向にはみ出していたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向にはみ出していたら
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20)) # 赤い爆弾の画像Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) # 赤い爆弾のRect
    bb_img.set_colorkey((0, 0, 0)) # 赤い爆弾の背景を透明にする
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    vx, vy = +20, +20   # 赤い爆弾の速度
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct): # こうかとんが赤い爆弾に当たったら
            return # ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy) 
        yoko, tate = check_bound(bb_rct)
        if not yoko: # 横方向にはみ出していたら
            vx *= -1
        if not tate: # 縦方向にはみ出していたら
            vy *= -1
        screen.blit(bb_img, bb_rct) # 赤い爆弾を画面に貼り付ける

        gameover(screen) if kk_rct.colliderect(bb_rct) else None # こうかとんが赤い爆弾に当たったらゲームオーバ

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
