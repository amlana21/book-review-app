const loginForm=document.querySelector('#login')
const loginbtn=document.querySelector('#usrnme')
const url=`${window.location.protocol}//${window.location.host}`
console.log(url)
loginForm.addEventListener('submit',async (e)=>{
    e.preventDefault()
    let usr=e.target.elements.usrnme.value
    let pswrd=e.target.elements.pswrd.value
    try{
        const getlogin=await fetch(`${url}/login`,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                username:usr,
                password:pswrd
            })
        })
        const loginJson=await getlogin.json()
        if(loginJson.login==='success'){
            window.location.reload()
        }else{
            throw new Error('Auth Failed')
        }
        console.log(loginJson)
    }catch(e){
        alert('Invalid Username or Password!!')
    }
})

var modal = document.getElementById("myModal");
document.querySelector('#regster').addEventListener('click',(e)=>{
    e.preventDefault()
    modal.style.display = "block";
})

var span = document.getElementsByClassName("close")[0];
span.onclick = function() {
    modal.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

//register form
document.querySelector('#registerfrm').addEventListener('submit',async (e)=>{
    e.preventDefault()
    const fname=e.target.elements.fname.value
    const lname=e.target.elements.lname.value
    const emailTxt=e.target.elements.email.value
    const uname=e.target.elements.uname.value
    const pwdTxt=e.target.elements.pwd.value
    try{
        const regResp=await fetch(`${url}/register`,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                firstname:fname,
                lastname:lname,
                email:emailTxt,
                username:uname,
                password:pwdTxt
            })
        })
        const regjson=await regResp.json()
        if(regjson.status==='success'){
            // alert('success')
            e.target.elements.fname.value=''
            e.target.elements.lname.value=''
            e.target.elements.email.value=''
            e.target.elements.uname.value=''
            e.target.elements.pwd.value=''
            modal.style.display = "none";
        }else if(regjson.error.includes('duplicate key')){
            alert('Username exists!!')
        }
    }catch(e){
        console.log(e.message)
        alert(e.message)
    }   

})