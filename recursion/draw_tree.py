import turtle

t = turtle.Turtle()
t.left(90)  # Point straight UP
t.speed(1)  # Fast animation


def draw_branch(length):
    if length < 30:  # Base case
        t.dot(12, "green")
        return

    t.forward(length)

    t.left(30)
    draw_branch(length * 0.7)  # Left sub-tree
    t.right(60)
    draw_branch(length * 0.7)  # Right sub-tree

    t.left(30)
    t.backward(length)  # Backtrack to junction point


draw_branch(200)
turtle.done()

