$('#spindiv').hide()
const srchfrm=document.querySelector('#srchfrm')
const srchTxt=document.querySelector('#srchtxt')
const url=`${window.location.protocol}//${window.location.host}`

srchfrm.addEventListener('submit',async (e)=>{
    e.preventDefault()
    $('.alert').hide()
    $('.alert').empty()
    $('#spindiv').show()
    let msgtble=document.getElementById('rslts')
    while(msgtble.hasChildNodes())
                {
                    msgtble.removeChild(msgtble.firstChild);
                }
    const srchUrl=`${url}/books/search?search=${srchTxt.value}`
    try{
        const srchOut=await fetch(srchUrl,{
            method:'GET'
        })
        const srchResp=await srchOut.json()
        if(srchResp.found==='none'){
            $('.alert').append('<strong>Error!!</strong>No books found!!')
            $('.alert').show()
            $('#spindiv').hide()
            return
        }
        console.log(srchResp)
        $('#spindiv').hide()
        //display
        srchResp.results.forEach((srch)=>{
            let nrow=`<tr><td><img src='${srch.pics[1]}'><td><a href='${url}/details?isbn=${srch.isbn}&picarr=${srch.pics}'>${srch.title}</a></td><td>${srch.author}</td><td>${srch.year}</td></tr>`
            $('#rslts').append(nrow)
        })
    }catch(e){
        alert(e.message)
    }
})