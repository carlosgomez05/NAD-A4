console.log('hello-world-detail')
const postBox = document.getElementById('post-box')
const alertBox = document.getElementById('alert-box')
const backBtn = document.getElementById('back-btn')
const updateBtn = document.getElementById('update-btn')
const deleteBtn = document.getElementById('delete-btn')

const url = window.location.href + "data/"
const updateUrl = window.location.href + "update/"
const deleteUrl = window.location.href + "delete/"

const updateForm = document.getElementById('update-form')
const deleteForm = document.getElementById('delete-form')

const spinnerBox = document.getElementById('spinner-box')

const titleInput = document.getElementById('id_title')
const bodyInput = document.getElementById('id_body')


const commentForm = document.getElementById('comment-form')
const commentBody = commentForm.querySelector('textarea')
const commentsBox = document.getElementById('comments-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')


$.ajax({
    type: 'GET',
    url: url,
    success: function(response) {
        console.log(response)
        const data = response.data

        if(data.logged_in !== data.author) {
            console.log('different')
        } else {
            console.log('the same')
            updateBtn.classList.remove('not-visible')
            deleteBtn.classList.remove('not-visible')
        }

        const authorDiv = document.createElement('div')
        authorDiv.setAttribute('class', 'author-info mb-4')
        authorDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="${data.avatar}" class="rounded-circle me-3" height="50" width="50" alt="${data.author}">
                <h6 class="mb-0">${data.author}</h6>
            </div>
        `
        
        const titleEl = document.createElement('h3')
        titleEl.setAttribute('class', 'mt-3')
        titleEl.setAttribute('id', 'title')

        const bodyEl = document.createElement('p')
        bodyEl.setAttribute('class', 'mt-1')
        bodyEl.setAttribute('id', 'body')

        titleEl.textContent = data.title
        bodyEl.textContent = data.body

        postBox.appendChild(titleEl)
        postBox.appendChild(bodyEl)

        titleInput.value = data.title
        bodyInput.value = data.body

        spinnerBox.classList.add('not-visible')
    },
    error: function(error) {
        console.log(error)
    }
})

updateForm.addEventListener('submit', e=>{
    e.preventDefault()

    const title = document.getElementById('title')
    const body = document.getElementById('body')

    $.ajax({
        type: 'POST',
        url: updateUrl,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'title': titleInput.value,
            'body': bodyInput.value,
        },
        success: function(response){
            console.log(response)
            handleAlerts('success', 'Post has been updated')
            title.textContent = response.title
            body.textContent = response.body
        },
        error: function(error){
            console.log(error)
        }
    })

})

deleteForm.addEventListener('submit', e=>{
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: deleteUrl,
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
        },
        success: function(response) {
            window.location.href = window.location.origin
            localStorage.setItem('title', titleInput.value)
        },
        error: function(error) {
            console.log(error)
        }
    })
})

commentForm.addEventListener('submit', e => {
    e.preventDefault()
    
    $.ajax({
        type: 'POST',
        url: window.location.href + 'comment/',
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'body': commentBody.value,
        },
        success: function(response) {
            commentsBox.insertAdjacentHTML('afterbegin', `
                <div class="card mb-2">
                    <div class="card-body">
                        <div class="d-flex mb-2">
                            <img src="${response.profile_pic}" class="rounded-circle me-2" width="30" height="30">
                            <div>
                                <h6 class="mb-0">${response.username}</h6>
                                <small class="text-muted">${response.created}</small>
                            </div>
                        </div>
                        <p class="card-text">${response.body}</p>
                    </div>
                </div>
            `)
            commentForm.reset()
            handleAlerts('success', 'Comment added successfully')
        },
        error: function(error) {
            console.log(error)
            handleAlerts('danger', 'Something went wrong')
        }
    })
})