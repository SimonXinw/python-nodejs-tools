(function () {

    function $(className) {

        return document.querySelector(className)


    }


    const mainEle = $('.Question-main')

    const btnEles = mainEle.querySelectorAll('.QuestionInvitation-content .List  .List-item .ContentItem-extra button')


    let time = 100

    btnEles.forEach(async element => {

        debugger

        const starTime = Date.now()

        while (Date.now() - starTime < time) {

        }

        time += 100

        element.click()

        console.log('看看这里的时间是多少，', time)

    });

})()