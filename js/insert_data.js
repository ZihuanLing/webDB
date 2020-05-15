const vm = new Vue({
    el: '#container',
    data: {
        db: '',
        sql: '',
        insertResult: '',
        insertDone: false,
        askExecute: true,
        record_id: -1,
        fields: {},
        column_description: [],
        column_detail: []
    },
    created: function () {
        let max_columns = 3;
        let that = this;
        let key_params = JSON.parse(window.atob(localStorage.getItem('key_params')));
        that.db = key_params.db;
        that.record_id = key_params.record_id;
        that.table = key_params.tbl;
        let column_description = JSON.parse(localStorage.getItem('column_description'));
        let data_description = JSON.parse(localStorage.getItem('data_description'));
        let column_detail = JSON.parse(localStorage.getItem('column_detail'));
        for (let i = 0; i < max_columns; i++) that.column_description.push(column_description[i][0]);
        column_detail.forEach(item => {
            that.fields[item[0]] = '';
            that.column_detail.push(item.splice(0, max_columns));
        });
        document.getElementsByTagName('title')[0].innerText = "插入" + this.db + '.' + this.table;
    },
    methods: {
        generate_sql: function () {
            // INSERT INTO `test` (`id`, `name`, `phone`, `age`, `gender`) VALUES (NULL, 'Oday', '13725761132', '13', 'male');
            let keys = [];
            let values = [];
            let fields = this.fields;
            for (let key in fields) {
                if (fields.hasOwnProperty(key)) {
                    keys.push("`" + key + "`");
                    values.push(fields[key] ? "\'" + fields[key] + "\'" : 'NULL');
                }
            }
            let sql = "INSERT INTO `" + this.table + "` (" + keys.join(',') + ") VALUES (" + values.join(',') + ");";
            this.sql = sql;
            this.insertDone = false;
            this.askExecute = true;
            document.getElementById('toggle-modal').click();
        },
        execute_insert: function () {
            let tsessionid = this.$cookies.get('tsessionid');
            let data = {
                record_id: this.record_id,
                command: this.sql,
            };
            let that = this;
            axios.post('/OperateDB/', data, {
                headers: {tsessionid: tsessionid}
            }).then((res) => {
                console.log(res);
                that.askExecute = false;
                that.insertDone = true;
                that.insertResult = "插入成功";
            }).catch(function (err) {
                console.log(err);
                that.askExecute = false;
                that.insertDone = true;
                that.insertResult = err.response.data['err_msg'];
                // if (err_msg) alert(err_msg);
            })
        }
    }
});