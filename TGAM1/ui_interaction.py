import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from plot import *


frame_size_x = 0.25
frame_size_y = 0.9
frame_width = 0.01

handle_size_x = 0.20
handle_size_y = 0.20
handle_border = 0.05

handle_pos_perc = 1.0


def clamp(value, min_v, max_v):
    return max(min_v, min(value, max_v))

def newPos1(payloadParser, handle_pos_perc):
    if payloadParser.attention > 0.5:
        return handle_pos_perc + 0.05
    else:
        return handle_pos_perc - 0.05
    
def newPos2(payloadParser, handle_pos_perc):
    if payloadParser.attention > payloadParser.meditation + 0.1:
        return handle_pos_perc + 0.05
    else:
        return handle_pos_perc - 0.05
    

def newHandlePos(payloadParser, handle_pos_perc):
    return clamp(newPos1(payloadParser, handle_pos_perc), 0.0, 1.0)


def drawRect(x, y, x_len, y_len):
    glBegin(GL_TRIANGLE_STRIP)
    glVertex2f(x, y)
    glVertex2f(x + x_len, y)
    glVertex2f(x, y + y_len)
    glVertex2f(x + x_len, y + y_len)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    glColor(0.0, 1.0, 0.0)
    drawRect(-frame_size_x, -frame_size_y, frame_size_x*2, frame_size_y*2)

    glColor(0.0, 0.0, 0.0)
    drawRect(-(frame_size_x-frame_width), -(frame_size_y-frame_width), (frame_size_x-frame_width)*2, (frame_size_y-frame_width)*2)

    handle_y_area_len = frame_size_y - handle_size_y - handle_border
    glColor(0.0, 1.0, 0.0)
    drawRect(-handle_size_x, -frame_size_y + handle_border + handle_pos_perc * 2 * handle_y_area_len, handle_size_x*2, handle_size_y*2)

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-1.0, 1.0, -1.0 / aspect_ratio, 1.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-1.0 * aspect_ratio, 1.0 * aspect_ratio, -1.0, 1.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



if __name__ == '__main__':
    parser = TGAMPacketParser()
    plot = Plot()  

    with serial.Serial(SERIAL_PORT, 9600, timeout=10) as ser:            
        if not glfwInit():
            sys.exit(-1)

        window = glfwCreateWindow(400, 400, __file__, None, None)
        if not window:
            glfwTerminate()
            sys.exit(-1)

        glfwMakeContextCurrent(window)
        glfwSetFramebufferSizeCallback(window, update_viewport)
        glfwSwapInterval(1)

        update_viewport(None, 400, 400)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        while not glfwWindowShouldClose(window):
            render(glfwGetTime())
            glfwSwapBuffers(window)
            #glfwPollEvents()

            byte = int.from_bytes(ser.read(1), "little")
            isValid, payload = parser.parseByte(byte)

            if isValid:
                payloadParser = TGAMPacketPayloadParser()
                payloadParser.parsePayload(payload)

                plot.update(payloadParser)

                handle_pos_perc = newHandlePos(payloadParser, handle_pos_perc)

            

        glfwTerminate()