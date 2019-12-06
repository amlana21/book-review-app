// console.log('loaded details..')
// console.log(`Book ID: ${bkid}`)
// console.log(`URL: ${pics.split(',')}`)
const url=`${window.location.protocol}//${window.location.host}`
const revwFrm=document.querySelector('#reviewfrm')
let bookId=''

//display pic
const picdiv=$('#imgdiv')
const picUrlDiv=pics.split(',')[0]
const picHtm=`<img class='bookimg' height="170" width="110" src='${picUrlDiv}'>`
picdiv.append(picHtm)

fetch(`${url}/api/${bkid}`,{method:'GET'}).then(async (resp)=>{
    let bookresp=await resp.json()
    bookId=bookresp.id
    const tbl=$('#detailtbl')
    let trow1=`<tr><td><strong>Book Name:</strong></td><td>${bookresp.title}</td></tr>`
    tbl.append(trow1)
    let trow2=`<tr><td><strong>Author:</strong></td><td>${bookresp.author}</td></tr>`
    tbl.append(trow2)
    let trow3=`<tr><td><strong>Publication Year:</strong></td><td>${bookresp.year}</td></tr>`
    tbl.append(trow3)
    let trow4=`<tr><td><strong>ISBN:</strong></td><td>${bookresp.isbn}</td></tr>`
    tbl.append(trow4)
    let trow5=`<tr><td><strong>Review Count:</strong></td><td>${bookresp.review_count}</td></tr>`
    tbl.append(trow5)
    let trow6=`<tr><td><strong>Avg. Rating:</strong></td><td>${bookresp.average_score}</td></tr>`
    tbl.append(trow6)
    //------------reviews
    const revOut=await fetch(`${url}/review/${bookId}`,{method:'GET'})
    const revResp=await revOut.json()
    if (revResp.error){
        const revDivE=$('#revErr')
        const revErr='<strong>No Reviews!</strong> found for this book.'
        revDivE.append(revErr)
        document.querySelector('#revErr').style.display='block'
        document.querySelector('.displayclass').style.display='none'
    }else if(revResp.length===0){
        
    }else{
    const revLst=$('#revtbl')
    revResp.forEach((rev)=>{
        let revRep='⭐'.repeat(parseInt(rev.rating))
        const revRow=`<tr><td>${revRep}</td><td>${rev.username}</td><td><p>${rev.review}</p></td></tr>`
        revLst.append(revRow)
    })
    }    

    //submit review
    revwFrm.addEventListener('submit',async (e)=>{
        e.preventDefault()
        const selected=document.querySelector('input[name=optradio]:checked').value
        const revStr=document.querySelector('#review').value
        const revSubmt=await fetch(`${url}/submit/review`,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                rating:selected,
                review:revStr,
                book_id:bookresp.id
            })
        })
        const revResp1=await revSubmt.json()
        if(revResp1.error){
            if(revResp1.error.includes('duplicate key')){
                return alert('You have already submitted review!!')
            }
        }

        //load table
        const revLst=$('#revtbl')
        let ratingRepeat='⭐'.repeat(parseInt(selected))
        const revRow1=`<tr><td>${ratingRepeat}</td><td>${revResp1.username}</td><td>${revStr}</td></tr>`
        revLst.prepend(revRow1)
        document.querySelector('#revErr').style.display='none'
        document.querySelector('.displayclass').style.display='block'

        //remove text
        document.querySelector('#review').value=''
        document.querySelector('input[name=optradio]:checked').checked=false
    })
}).catch((e)=>{
    if(e.message.includes('duplicate key')){
        alert('You have already submitted review!!')
    }else{
        alert(e.message)
        console.log(e.message)
    }
})