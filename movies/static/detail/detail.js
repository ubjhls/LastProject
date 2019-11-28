starRating();

$("#ale").on('hidden.bs.modal', function (e) {
 
  $("#ale iframe").attr("src", $("#ale iframe").attr("src"));
 });

 <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
 const likeButton = document.querySelector('#like-button')
 likeButton.addEventListener('click', function (event) {
   console.log(event.target.dataset)
   axios.defaults.xsrfCookieName = 'csrftoken'
   axios.defaults.xsrfHeaderName = 'X-CSRFToken'
   axios.defaults.headers.common['X-REQUESTED-WITH'] = 'XMLHttpRequest'
   axios.post(`/movies/${event.target.dataset.id}/like/`)
     .then(response => {
       const likeCount = document.querySelector('#like-count')
       console.log(response)
       console.log(event.target)
       if (response.data.is_liked) {
         event.target.classList.remove('far')
         event.target.classList.add('fas')
       } else {
         event.target.classList.remove('fas')
         event.target.classList.add('far')
       }
       likeCount.innerText = response.data.like_count
     })
     .catch(error => {
       console.log(error)
     })
 })
 $('.starRev span').click(function () {
   $(this).parent().children('span').removeClass('on');
   $(this).addClass('on').prevAll('span').addClass('on');
   return false;
 });

