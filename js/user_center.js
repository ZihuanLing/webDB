axios.defaults.baseURL = 'http://127.0.0.1:8888/';
vm = new Vue({
    el: "#wrapper",
    data: {
        nick_name: 'Nobody',
        recordDatas: [],
        del_id: null
    },
    created() {
        this.fetchRecord()
    },
    methods: {
        logout(){
            this.$cookies.remove('tsessionid');
            location.href = "/";
        },
        delRecord: function (record_id = this.del_id) {
            if (this.del_id) {
                console.log("deleting : ", record_id)
                let tsessionid = this.$cookies.get('tsessionid');
                axios.get("/DelRecord/" + record_id, {
                    headers: {
                        tsessionid: tsessionid
                    }
                }).then(res => {
                    console.log(res.data);
                    if (res.status == 200) {
                        this.hideConfirm();
                        alert("删除成功")
                    } else {
                        alert("删除出错")
                    }
                    this.fetchRecord();
                }).catch(err => {
                    console.log(err);
                })
            }

        },
        fetchRecord: function () {
            let tsessionid = this.$cookies.get('tsessionid');
            if (tsessionid) {
                axios.get("/DBRecord/", {
                    headers: {
                        tsessionid: tsessionid
                    }
                }).then(res => {
                    this.recordDatas = res.data;
                }).catch(err => {
                    console.log(err);
                })
            } else {
                console.log("没有tsessionid")
            }
        },
        showConfirm: function (record_id) {
            $("#sweet-alert-container")[0].hidden = false;
            this.del_id = record_id;
        },
        hideConfirm: function () {
            $("#sweet-alert-container")[0].hidden = true;
            this.del_id = null;
        },
        connectDB: function (record_id, database) {
            // console.log("record id is : ", record_id);
            params = {record_id: record_id, database: database};
            params = window.btoa(JSON.stringify(params));
            window.location.href = "/html/database.html?_=" + params;
        }
    }
});

function confirmDelete() {
    vm.delRecord();
}

function cancelDelete() {
    vm.hideConfirm();
}