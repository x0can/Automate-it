window.onload = function() {
    document.getElementById('ifYes').style.display = 'none';
    document.getElementById('ifNo').style.display = 'none';
    document.getElementById('submit').style.display='none';
}



function yesnoCheck() {
    if (document.getElementById('yesCheck').checked) {
        document.getElementById('ifNo').style.display = 'block';
        document.getElementById('ifYes').style.display = 'none';
        document.getElementById('owner').style.display = 'none';
        
        
    } 
    else if(document.getElementById('noCheck').checked) {
        document.getElementById('ifYes').style.display = 'block';
        document.getElementById('ifNo').style.display = 'none';
        document.getElementById('owner').style.display = 'block';
   }
}