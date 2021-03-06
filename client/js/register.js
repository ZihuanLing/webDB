// /**
//  * Created by Think on 2018/7/7.
//  */

axios.defaults.baseURL = 'http://127.0.0.1:8888/';
new Vue({
    el:"#content",
    data:{
        mobile:'',
        password:'',
        code:'',
        errEmail:'',
        countDown:'',
        getCodes:true,
        datacode:'',
    },
    methods: {
        //提交表单
        submit: function () {

            const that =this;
            if (this.password.length >= 6 && this.password.length <= 16 && this.code.length === 4) {
                  axios.post('/register/',{
                    'email':that.email,
                    'code':that.code,
                    'password':that.password
                }).then((res)=>{
                    alert('注册成功，点击确定去登录');
                      location.href = './login.html';
                }).catch((err)=>{
                      if(err.response.status === 403 || err.response.status === 400){
                          if(err.response.data.code){
                              that.datacode = err.response.data.code
                          }else if(err.response.data.email){
                              that.dataEmail = err.response.data.email
                          }
                      }

                  })
            } else {
                alert('请填写正确信息！')
            }

        },
        //验证邮箱
        changeMobile: function () {
            const that = this;
            let reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            let res = reg.test(that.email);
            if (!res) {
                this.errEmail = '请输入正确的邮箱'
            } else {
                this.errEmail = ''

            }
        },
        //获取验证码+执行倒计时
        getCode: function () {
            const that = this;
            let reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            let res = reg.test(that.email);
            if (!res) {
                this.errEmail = '请输入正确的邮箱'
            } else {
                //执行倒计时
                that.getCodes = false;
                that.countDown = 60;

                let timer = setInterval(function () {
                    that.countDown -= 1;
                    if(that.countDown === 0){
                        clearInterval(timer);
                        that.getCodes = true;
                        that.countDown = false
                    }
                },1000);
                that.countDown = 60;

                axios.post('/code/', {
                    'email': that.email
                }).then((res) => {
                    console.log(res)
                }).catch((err) => {
                    if (err.response.data.email) {
                        that.errEmail = err.response.data.email;
                    }
                })
            }
        }
    }
});





