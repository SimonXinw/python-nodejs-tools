(function () {
    // 引入SheetJS库的函数
    function loadSheetJS(callback) {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js';
        script.onload = callback;
        document.head.appendChild(script);
    }

    // 检查页面加载完成并且提取院校名称的函数
    function checkAndSaveData(url) {
        return new Promise((resolve, reject) => {
            // 假设这里使用了某种方式来加载页面，例如: fetch 或者直接在新标签页打开
            // 这里使用setTimeout模拟页面加载过程
            setTimeout(() => {
                // 检查url是否改变，这里需要根据实际页面加载后的URL进行判断
                if (window.location.href !== url) {
                    console.error('URL错误');
                    reject('URL错误');
                    return;
                }

                // 检查院校名称是否存在
                const schoolName = document.querySelector('.school-tab_name__3pOZK')?.innerText;
                if (schoolName) {
                    const院校代码 = 1; // 假设院校代码是1，这里需要根据实际情况赋值
                    const dataRow = [schoolName, 院校代码];
                    resolve(dataRow);
                } else {
                    console.error('院校名称不存在');
                    reject('院校名称不存在');
                }
            }, 3000); // 假设页面加载需要3秒
        });
    }

    // 主循环函数
    async function mainLoop() {
        const baseUrls = [
            'https://www.gaokao.cn/school/1/provinceline',
            'https://www.gaokao.cn/school/2/provinceline',
            // 更多URL...
        ];

        const formatData = [];

        for (let i = 0; i < 5000; i++) { // 执行5000次循环
            const url = baseUrls[i % baseUrls.length]; // 循环使用baseUrls数组中的URLs

            console.log(`正在处理第 ${i + 1} 次循环，URL: ${url}`);

            // 这里需要使用某种方式打开URL，例如: window.open 或者其他方式
            // 然后切换到新标签页并等待页面加载
            const dataRow = await checkAndSaveData(url).catch(error => {
                console.error(error);
                // 如果页面加载失败或URL错误，存储错误信息并继续循环
                const errorRow = ['错误信息', ''];
                formatData.push(errorRow);
                continue;
            });

            if (dataRow) {
                formatData.push(dataRow);
            }
        }

        // 所有页面处理完毕后，转换数据为Excel文件
        loadSheetJS(() => {
            const ws = XLSX.utils.aoa_to_sheet(formatData);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
            XLSX.writeFile(wb, '院校招生专业组专业明细.xlsx');
        });
    }

    // 执行主循环
    mainLoop();
})()