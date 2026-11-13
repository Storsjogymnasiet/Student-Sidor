const timerDisplay = document.getElementById('timer');
const scoreDisplay = document.getElementById('score');
const targetBall = document.getElementById('target-ball');
const playArea = document.getElementById('play-area');
const resetBtn = document.getElementById('reset-btn');

let score = 0;
let timerleft = 50;
let timerintervals = null;
let gameintervals = null;


function moveBall() {
    const maxY = 350;
    const maxX = 350;


    const randomX = Math.floor(Math.random() * maxY);
    const randomY = Math.floor(Math.random() * maxX);



    targetBall.style.left = randomX + 'px';
    targetBall.style.top = randomY + 'px';


}

targetBall.addEventListener('click', () => {

    score++;


    scoreDisplay.textContent = score;
    moveBall();



});




function startgame() {

    score = 0;
    timerleft = 50;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timerleft;
    resetBtn.style.display = 'none';

    moveBall();

    timerintervals = setInterval(() => {

        timerleft--;
        timerDisplay.textContent = timerleft;

        if (timerleft <= 0) {
            endgame();
        }

    }, 1000);

}


function endgame() {
    clearInterval(timerintervals);
    targetBall.style.display = 'none';
    resetBtn.style.display = 'block';

}

resetBtn.addEventListener('click', () => {

    targetBall.style.display = 'block';
    startgame();
});

startgame();
