# Pycasso

Provides an interface to render frames on a browser, from you python program.

I want to keep this as close to the natural python experience, so no compilation step. I want it to be able to run in any modern operating system without having to think much about it.
For those reasons I will be using websockets and the browser to do the drawing.

When you run your program, initialize Pycasso. In that init step, Pycasso will:

1. Start a static file server on port 3000 so that browser can request the initial html, css, and js.
2. Start a websocket server at port 3001 that the user can connect to and receive updated frames
3. Open a browser window at port 3000
4. From the browser, connect to the websocket server 3001 with Javascsript

While your program is running, you can enqueue drawing command like :

```
ctx.SetFillStyle(color.RGBA{R: 200, A: 255})
ctx.FillRect(10, 10, 50, 50)
```

Once all the commmands for a single frame have been enqueued, you need to flush the queue with the `draw()` command. The Pycasso server will send a binary representation of the commands to the browser, all at once (FUTURE: Stream commands so that we can draw more complex frames).
The browser will then decode the commands into the Canvas API commands and execute them in order to render the scene.
