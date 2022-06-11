const $token = document.getElementById('token');
const $btn = document.getElementById('btn');
$btn.addEventListener('click', e => {

        $token.select();
        document.execCommand('copy');
})

