axios.defaults.baseURL = 'http://127.0.0.1:8888/';
vm = new Vue({
    el: "#wrapper",
    data: {
        nick_name: 'Nobody',
        host: '',
        port: 3306,
        user: '',
        password: '',
        database: '',
        note: '',
        db_type: 'MYSQL',
        db_types: ['MYSQL', 'MongoDB'],
        invalidate_host: false,
        invalidate_user: false,
    },
    methods: {
        logout() {
            this.$cookies.remove('tsessionid');
            location.href = "/";
        },
        checkHost: function () {
            if (this.host.length == 0) {
                this.invalidate_host = true;
            } else this.invalidate_host = false;
        },
        submit: function () {
            console.log('trying to submit')
            let data = {
                host: this.host,
                port: this.port,
                user: this.user,
                password: this.password,
                database: this.database,
                note: this.note,
                db_type: this.db_type,
            };
            let tsessionid = this.$cookies.get('tsessionid');
            if (tsessionid) {
                axios.post('/DBRecord/', data, {
                    headers: {tsessionid: tsessionid}
                }).then((res) => {
                    console.log(res.data);
                    if (res.status === 200) {
                        alert("创建成功。");
                        location.href = "/html/user-center.html";
                    }
                }).catch(function (err) {
                    console.log(err);
                    let err_msg = err.response.data['err_msg'];
                    if (err_msg) alert(err_msg);
                })
            } else {
                location.href = "../login.html"
            }
        }
    }
})