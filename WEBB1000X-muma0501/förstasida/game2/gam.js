const minutesDisplay = document.getElementById('minutes');
const secondsDisplay = document.getElementById('seconds');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const resetBtn = document.getElementById('reset-btn');
const workmodeBtn = document.getElementById('work-mode');
const breakmodeBtn = document.getElementById('break-mode');




let timerleft = 21 * 60;
let timerid = null;
let isRunnig = false;




function updateDIsplay() {
    const minutes = Math.floor(timerleft / 60);
    const seconds = Math.floor(timerleft % 60);

    minutesDisplay.textContent = String(minutes).padStart(2, '0');
    secondsDisplay.textContent = String(seconds).padStart(2, '0');

}

updateDIsplay();


function startTimer() {
    if (isRunnig)
        return;

    isRunnig = true;

    startBtn.disabled = true;
    pauseBtn.disabled = false;


    timerid = setInterval(() => {

        if (timerleft > 0) {
            timerleft--;
            updateDIsplay();


        }
        else {
            clearInterval(timerid);
            isRunnig = false;
            alert('time is up go drink water');
            resetTimer();
        }
    }, 1000);
}

function resetTimer() {
    isRunnig = false;
    timerleft = 0;
    updateDIsplay();

    resetTimer.disabled = false;
    breakmodeBtn.disabled = true;


}



function breakmodeBtn() {
    clearInterval(timerid);
    isRunnig = false;
    timerleft = 0;
    updateDIsplay();

}

startBtn.addEventListener('click', startTimer);


