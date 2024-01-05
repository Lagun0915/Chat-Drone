from PIL import Image, ImageDraw

def flight_path(path, file_name):
    # path는 비행 경로를 2차원 행렬로 입력받음.
    xy = {0:[1,0], 1:[0,1], 2:[-1,0], 3:[0,-1]}

    # 맵 만들기 + 안전 구역 그리기.
    img = Image.new('RGB', (500, 500), color = 'white')
    draw = ImageDraw.Draw(img)

    draw.rectangle([90, 90, 410, 410], outline='blue', width=5)

    # 드론의 시작 위치.
    pre_position=[100,100]
    pre_angle = 0

    for pin in path:
        angle, distance = pin
        x,y = xy[(pre_angle+angle)//90%4]
        x=x*distance; y=y*distance
        
        # 비행 경로는 빨간색으로 그림.
        draw.line((pre_position[0], pre_position[1],pre_position[0]+x,pre_position[1]+y),
                fill='red', width=5)
        
        pre_position[0]+=x; pre_position[1]+=y
        pre_angle=(pre_angle+angle)%360

    img.save(f'flight_path_{file_name}.png')
    # img.show()

    return img