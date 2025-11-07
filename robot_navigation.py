import pygame
import time
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# --- 1. กำหนดค่าคงที่ ---
# ขนาดของแต่ละช่อง (pixel)
CELL_SIZE = 30 
# จำนวนช่อง (กว้าง x สูง)
GRID_WIDTH = 20 
GRID_HEIGHT = 15

# ขนาดหน้าจอ (คำนวณอัตโนมัติ)
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# สี (RGB)
COLOR_WHITE = (255, 255, 255) # 0 = พื้นที่ว่าง
COLOR_BLACK = (40, 40, 40)    # 1 = สิ่งกีดขวาง (ผนัง)
COLOR_GREEN = (0, 255, 0)     # S = จุดเริ่มต้น (Start)
COLOR_RED = (255, 0, 0)       # E = เป้าหมาย (End)
COLOR_BLUE = (0, 150, 255)    # R = หุ่นยนต์ (Robot)
COLOR_YELLOW = (255, 254, 160) # P = เส้นทาง (Path)

# --- 2. กำหนดแผนที่ ---
# "แผนที่โกดัง"
# 0 = พื้นที่ว่าง, 1 = สิ่งกีดขวาง
MAP_GRID = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 'S', 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 'E', 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# --- 3. ฟังก์ชันวาดแผนที่ ---
def draw_grid(screen, grid_data):
    for y, row in enumerate(grid_data): # y แถว
        for x, cell in enumerate(row):  # x คอลัมน์
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            color = COLOR_WHITE
            if cell == 1:
                color = COLOR_BLACK
            elif cell == 'S':
                color = COLOR_GREEN
            elif cell == 'E':
                color = COLOR_RED
            elif cell == 'P': # Path
                color = COLOR_YELLOW
            elif cell == 'R': # Robot
                color = COLOR_BLUE
                
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLOR_BLACK, rect, 1) # วาดเส้นกริด

# --- 4. ฟังก์ชันหาพิกัด (Start/End) ---
def find_coordinates(grid_data, char):
    for y, row in enumerate(grid_data):
        for x, cell in enumerate(row):
            if cell == char:
                return (x, y) # คืนค่าเป็น (x, y)
    return (None, None)

# --- 5. ฟังก์ชันคำนวณเส้นทาง ---
def find_path(grid_data):
    # แปลง MAP_GRID (ที่มี S, E) ให้เป็น Matrix 0, 1
    # ที่ Library Pathfinding อ่านเข้าใจ (1 = เดินได้, 0 = เดินไม่ได้)
    matrix = []
    for row in grid_data:
        new_row = []
        for cell in row:
            if cell == 1:
                new_row.append(0) # 0 = Wall
            else:
                new_row.append(1) # 1 = Walkable
        matrix.append(new_row)

    # สร้าง Grid object
    grid = Grid(matrix=matrix)
    
    # หาพิกัด (x, y)
    start_x, start_y = find_coordinates(grid_data, 'S')
    end_x, end_y = find_coordinates(grid_data, 'E')

    if start_x is None or end_x is None:
        print("Error: ไม่พบจุด Start หรือ End")
        return None

    # สร้าง Node เริ่มต้นและเป้าหมาย
    start_node = grid.node(start_x, start_y)
    end_node = grid.node(end_x, end_y)

    # สร้างตัวค้นหา (AStarFinder)
    finder = AStarFinder()
    
    # คำนวณเส้นทาง!
    path, runs = finder.find_path(start_node, end_node, grid)
    
    if not path:
        print("Error: หาเส้นทางไม่พบ!")
        return None
        
    print(f"Path found! Length: {len(path)} steps. Runs: {runs}")
    return path

# --- 6. ส่วนหลักของโปรแกรม (Main) ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Robot Navigation (A* Algorithm)")
    
    # สร้าง copy ของแผนที่ไว้ใช้งาน (จะได้ไม่ทับ S, E)
    running_grid = [row[:] for row in MAP_GRID] 
    
    # 1. คำนวณเส้นทาง (เรียก AI)
    path = find_path(MAP_GRID)
    
    if not path:
        return # ถ้าหาทางไม่เจอ ก็ไม่ต้องทำต่อ

    # 2. วาดเส้นทางที่คำนวณได้ (สีเหลือง)
    for x, y in path:
        if running_grid[y][x] == 0: # ไม่ทับ S กับ E
            running_grid[y][x] = 'P' # P = Path
    
    # 3. วาดแผนที่ + เส้นทาง
    draw_grid(screen, running_grid)
    pygame.display.flip()

    # 4. แสดงการเคลื่อนที่ของหุ่นยนต์ (Animation)
    robot_pos = path[0] # ตำแหน่งปัจจุบันของหุ่นยนต์
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if path:
            # ย้ายหุ่นยนต์ไปตำแหน่งถัดไป
            robot_pos = path.pop(0) # ดึงตำแหน่งแรกออกจาก list
            x, y = robot_pos
            
            # เปลี่ยนตำแหน่งเก่า (ถ้าเคยเป็น R) กลับเป็น P
            for y_r, row in enumerate(running_grid):
                for x_r, cell in enumerate(row):
                    if cell == 'R':
                        running_grid[y_r][x_r] = 'P'
            
            # อัปเดตตำแหน่งใหม่ของหุ่นยนต์
            running_grid[y][x] = 'R' # R = Robot
            
            # วาดใหม่ทั้งหมด
            draw_grid(screen, running_grid)
            pygame.display.flip() # อัปเดตหน้าจอ
            
            # หน่วงเวลา
            time.sleep(0.1) # 0.1 วินาที
        else:
            # ถ้า path หมดแล้ว (ถึงที่หมาย)
            print("ถึงเป้าหมายแล้ว!")
            time.sleep(2) # รอ 2 วิ แล้วค่อยปิด
            running = False

    pygame.quit()

# --- รันโปรแกรม ---
if __name__ == "__main__":
    main()