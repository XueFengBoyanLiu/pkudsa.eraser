// Set a default speed scale for replay
speedScale=1;



initial={
  "boardSize": 8,
  "totalFrames": 100,
  "frames": [
    {

    },
    {

    },
    {

    },
    {

    }
  ]
}


// Get the size of the board and the total number of frames
boardSize=initial.boardSize;
totalFrames=initial.totalFrames;

// Define a function to draw the frame
function drawFrame(frameData) {

}


// Define an inital value for frame
let frame = 1;
// Define a function to play the animation
function play() {
  while (frame<=totalFrames) {
    // Get the frame data
    frameData=initial.Frames[frame-1];
    // Draw the frame
    drawFrame(frameData);
    // Increment the frame
    frame++;
    // Wait for the next frame
    sleep(1000/speedScale);
  }
}






