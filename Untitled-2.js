
async function getText(file) {
    let myObject = await fetch(file);
    let myText = await myObject.text();
    document.getElementById("demo").innerHTML = myText;
  }



//test()
getText('fetch_info.txt')