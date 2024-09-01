(async function() {
    const urls = Array.from({ length: 5000 }, (_, i) => `https://www.gaokao.cn/school/${i + 1}/provinceline`);
    const results = [['院校名称', '院校代码']];
    const failedResults = [['URL', '错误信息']];

    // 等待元素更新的函数，使用 MutationObserver
    function waitForElementUpdate(selector, timeout = 5000) {
        return new Promise((resolve, reject) => {
            const targetElement = document.querySelector(selector);
            if (!targetElement) {
                reject(new Error('目标元素未找到！'));
                return;
            }

            let timer;
            let observer;
            let debounceTimer;

            const timeoutHandler = () => {
                observer.disconnect();
                reject(new Error('等待更新超时！'));
            };                                                                                  
            const observerHandler = (mutationsList) => {
                if (debounceTimer) {
                    clearTimeout(debounceTimer);
                }
                debounceTimer = setTimeout(() => {
                    observer.disconnect();
                    resolve(true);
                }, 300);  // 防抖时间设为300ms
            };

            timer = setTimeout(timeoutHandler, timeout);
            observer = new MutationObserver(observerHandler);
            observer.observe(targetElement, { attributes: true, childList: true, subtree: true });
        });
    }

    for (const url of urls) {
        try {
            // 导航到新页面
            window.location.href = url;

            // 等待页面加载完成
            await waitForElementUpdate('.school-tab_name__3pOZK', 10000);

            // 检查页面元素
            const schoolName = document.querySelector('.school-tab_name__3pOZK')?.innerText;
            const schoolCode = url.match(/school\/(\d+)\//)[1];

            if (schoolName) {
                results.push([schoolName, schoolCode]);
            } else {
                failedResults.push([url, '院校名称未找到']);
            }
        } catch (error) {
            failedResults.push([url, error.message]);
        }
    }

    const formatData = results.concat(failedResults);

    // 2. 引入SheetJS库
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js';
    script.onload = () => {
        // 3. 数据转化为Excel文件
        const ws = XLSX.utils.aoa_to_sheet(formatData);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

        // 4. 下载Excel文件
        XLSX.writeFile(wb, '院校信息.xlsx');
    };
    document.head.appendChild(script);
})();
