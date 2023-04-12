const dustbins = document.querySelectorAll('.dustbin');
var a = document.getElementById("aa").value;
var b = document.getElementById("bb").value;
var c = document.getElementById("cc").value;
a = parseInt(a);
b = parseInt(b);
c = parseInt(c);
const levels = [a / 100, b / 100, c / 100];
function setTrashLevel(index, level) {
    const trashLevel = dustbins[index].querySelector('.trash-level');
    trashLevel.style.height = `${level * 100}%`;
    const percentage = Math.round(level * 100);
    trashLevel.setAttribute('data-percentage', `${percentage}%`);
}

function updateTrashLevels() {
    levels.forEach((level, index) => {
        setTrashLevel(index, level);
    });
}

updateTrashLevels();

setInterval(() => {
    levels.forEach((level, index) => {
        level += Math.random() * 0.2 - 0.1;
        level = Math.max(Math.min(level, 1), 0);
        levels[index] = level;
        setTrashLevel(index, level);
    });
}, 2000);

