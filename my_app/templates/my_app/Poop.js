let x;
let p;

let f1=function(){

x=prompt("Предлагаю сыграть в игру. Компьютер загадал число от 1 до 10. Попробуй угадать!")
document.getElementById("insert").classList.add("show");
let rand=Math.floor(Math.random() * Math.floor(10));
if (x==rand){
    document.getElementById("insert").innerHTML='Молодец, ты угадал!'
}
else{
    document.getElementById("insert").innerHTML='Упс, не угадал, компьютер загадал '+ rand + '. Попробуй ещё!'


}
}

let i=0;
let f2=function(){

i+=1;

if (i%2==0){
    document.getElementById("insert1").style.color="black";
    document.getElementById("insert1").style.background=" #FFFFCC";
}
else {
    document.getElementById("insert1").style.background="pink";
};

if (i==1){
    document.getElementById("insert1").innerHTML ='You click '+ i + ' time';
}
else{
    document.getElementById("insert1").innerHTML ='You click '+ i + ' times';
};
}

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
  }

let ff1=function() {
    document.getElementById("insert2").style.fontFamily = "Impact,sans-serif";

}

let ff2=function() {
    document.getElementById("insert2").style.fontFamily = "Courier New, monospace";
    
}

let ff3=function() {
    document.getElementById("insert2").style.fontFamily = "Bradley Hand, cursive";
    
}
