let x;
let p;

let f1=function(){

x=prompt("Предлагаю сыграть в игру. Компьютер загадал число от 1 до 10. Попробуй угадать!")
if (x==1 || x>=5){
    p='Молодец, ты покакал '+x+' раз!';
    document.getElementById("insert").style.color="yellow";
    document.getElementById("insert").style.background="blue";
}
    
else if (x>0 && (x>=2 || x<=4)){
    p='Молодец, ты покакал '+x+' раза!';
    document.getElementById("insert").style.color="yellow";
    document.getElementById("insert").style.background="blue";
}

else {
    p='Беги какать!'
    document.getElementById("insert").style.color="red";
    document.getElementById("insert").style.background="black";
}
document.getElementById("insert").innerHTML = p;

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
