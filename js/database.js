axios.defaults.baseURL = 'http://127.0.0.1:8888/';
vm = new Vue({
    el: "#wrapper",
    data: {
        command: "",
        nick_name: 'Nobody',
        record_id: -1,
        columns: [],
        data: [],
        column_description: [],
        column_detail: [],
        data_detail: [],
        data_description: [],
        table: '',
        database: '',
        tables: [],
        pages: [5, 10, 20, 50],
        selectId: 1,
        page: 10,       // 每一页显示数量
        pageIdx: 1,      // 当前页面
        totalPages: 0
    },
    created() {
        let url = window.location.href;
        let params = url.split("?")[1].slice(2);
        params = JSON.parse(window.atob(params));
        this.record_id = params.record_id;
        this.database = params.database;
        // console.log(params);
        let that = this;
        // 获取当前所有数据库的tables；
        this.execute_sql("show tables;", re_data => {
            let res = re_data['result'];
            res.forEach(tb => that.tables.push(tb[0]));
            // 设置第一个table为默认
            if (that.tables) {
                that.table = that.tables[0];
                // that.table = 'db';
                that.fetch_columns();
                that.fetch_data();
            }
        });
    },
    methods: {
        logout() {
            this.$cookies.remove('tsessionid');
            location.href = "/";
        },
        pageChange: function (val) {
            this.pageIdx += val;
            if (this.pageIdx <= 0) this.pageIdx = 1;
            if (this.pageIdx >= this.totalPages) this.pageIdx = this.totalPages;
            // console.log(this.pageIdx);
        },
        splitPage: function () {
            this.page = this.pages[this.selectId];
            this.totalPages = Math.ceil(this.data.length / this.page);
            if (this.pageIdx > this.totalPages) this.pageIdx = this.totalPages;
        },
        format_columns: function (cols, datas) {
            // console.log("Is formatting the columns;");
            // console.log(cols);
            // console.log(datas);
            let columns = [];
            let data = [];
            let that = this;

            cols.forEach(item => {
                columns.push({title: item[0], key: item[0], sortable: true})
            });
            datas.forEach(item => {
                let tmp = {};
                for (let i in cols) tmp[cols[i][0]] = item[i];
                data.push(tmp)
            });
            that.columns = columns;
            that.data = data;
            that.totalPages = Math.ceil(that.data.length / that.page);
        },
        showConfirm: function (record_id) {
            $("#sweet-alert-container")[0].hidden = false;
        },
        hideConfirm: function () {
            $("#sweet-alert-container")[0].hidden = true;
        },
        execute_sql: function (sql, callback) {
            let tsessionid = this.$cookies.get('tsessionid');
            let data = {
                record_id: this.record_id,
                command: sql,
            };
            axios.post('/OperateDB/', data, {
                headers: {tsessionid: tsessionid}
            }).then((res) => {
                if (callback) callback(res.data)
            }).catch(function (err) {
                console.log(err);
                let err_msg = err.response.data['err_msg'];
                if (err_msg) alert(err_msg);
            })
        },
        run_command: function (obj) {
            if (!this.command) return;
            let that = this;
            that.execute_sql(this.command, re_data => {
                that.data_description = re_data['description'];
                that.data_detail = re_data['result'];
                if (that.data_detail.length === 0) {
                    that.fetch_data();
                }
                that.format_columns(re_data['description'], re_data['result']);
            });
        },
        fetch_columns: function (callback) {
            // 获取当前table的所有columns
            let that = this;
            if (callback) {
                that.execute_sql("show columns from " + that.table, callback)
            } else {
                that.execute_sql("show columns from " + that.table, (re_data => {
                    that.column_description = re_data['description'];
                    that.column_detail = re_data['result'];
                }))
            }
        },
        fetch_data: function (table) {
            // 获取当前database.table的所有数据
            let that = this;
            if (table) {
                that.table = table;
            }
            // let command = "select * from " + that.database+'.'+that.table;
            let command = "select * from " + that.table;
            that.execute_sql(command, re_data => {
                that.format_columns(re_data['description'], re_data['result'])
            });
            that.fetch_columns();
        },
        view_structure: function () {
            let elem = $("#command-input")[0];
            if (!elem.hidden) elem.hidden = true;
            let that = this;
            that.fetch_columns(re_data => {
                that.format_columns(re_data['description'], re_data['result'])
            })
        },
        toggle_command_input: function () {
            let elem = $("#command-input")[0];
            elem.hidden = !elem.hidden;
        },
        append_command: function (command) {
            this.command += command;
        },
        reset_command: function () {
            this.command = "";
        },
        insert_data: function () {
            this.fetch_columns();
            let key_params = {db: this.database, record_id: this.record_id, tbl: this.table};
            localStorage.setItem('key_params', window.btoa(JSON.stringify(key_params)));
            localStorage.setItem('column_description', JSON.stringify(this.column_description));
            localStorage.setItem('data_description', JSON.stringify(this.data_description));
            localStorage.setItem('column_detail', JSON.stringify(this.column_detail));
            window.open('/html/insert_data.html');
        }
    }
});

function confirmDelete() {
    vm.delRecord();
}

function cancelDelete() {
    vm.hideConfirm();
}