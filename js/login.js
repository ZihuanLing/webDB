/**
 * Created by Think on 2018/7/6.
 */
axios.defaults.baseURL = 'http://127.0.0.1:8888/';
var vm = new Vue({
    el:'#content',
    data:{
        email:'',
        password:'',
        account:false,
        datapsw:'',
        dataemail:''
    },
    created(){
        let tsessionid = this.$cookies.get("tsessionid");
        console.log(tsessionid)
        if (tsessionid){
            axios.get("/", {
                headers: {
                    "tsessionid": tsessionid
                }
            }).then(response => {
                console.log(response)
                re_data = response.data;
                if (re_data.verify_status == 'OK'){
                    // location.href = re_data.redirect;
                }
            })
        }
    },
    methods:{
        login: function() {
            // this.getcookie();
            let that = this;
            let reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            if(!reg.test(that.email) || this.password.length < 6 || this.password.length>20){
                alert('请填写正确的信息！')
            }else{
                axios.post('/login/',{
                    'email':that.email,
                    'password':that.password
                }).then((res)=>{

                    console.log(res.data);
                    this.$cookies.set('tsessionid',res.data.token);
                    this.$cookies.set('nick_name',res.data.nick_name);
                    this.$cookies.set('user_id',res.data.id);
                    location.href = '/html/user-center.html';
                    console.log("Login ok")
                }).catch(function (err) {
                    console.log(err);
                    if(err.response.status === 400){
                        if(err.response.data.non_fields){
                            that.datapsw = err.response.data.non_fields;
                            that.dataemail = ''
                        }else if(err.response.data.email){
                            that.datapsw = '';
                            that.dataemail = err.response.data.email
                        }
                    }
                })
            }
        },
        changeemail:function(){
            let that = this;
            let reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
            if(!reg.test(that.email)){
                this.account = '请输入正确的邮箱!';
            }else{
                that.account = '';
            }
        },
        setCookie:function (userId) {
            let str = 'token = '+userId;
            document.cookie = str;
        },
        getcookie:function () {
            let cookies = document.cookie;
            let cookiesArr = cookies.split(';');
            cookiesArr.forEach(function (value, index, array) {
                var a = 'userId';
               if(value.indexOf(a)){
                   console.log(value);
                    return
               }
            });
        }
    }
});

