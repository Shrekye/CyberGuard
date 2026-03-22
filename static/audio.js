const music= document.getElementById("audio");
const icon= document.getElementById("musicIcone");
const volumeSlider = document.getElementById('volume');
const playbtn= document.getElementById("play");
const pausebtn=document.getElementById("pause");

playbtn.style.display = "block";
pausebtn.style.display = "none";
function toggleMusic() {
    if (music.paused){
        music.play();
        playbtn.style.display = "none";
        pausebtn.style.display = "block";
    }
    else{
        music.pause();
        playbtn.style.display = "block";
        pausebtn.style.display = "none";
    }
}

volumeSlider.addEventListener('input', (e) => {
    music.volume = e.target.value;
});
document.addEventListener('click', ()=> {}, {once: true}); 