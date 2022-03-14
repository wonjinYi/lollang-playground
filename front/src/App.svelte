<script>
	import { writable } from 'svelte/store';

	import axios from 'axios';
	import { saveAs } from 'file-saver';
	import SvelteTooltip from 'svelte-tooltip';

	import CompileMode from './components/CompileMode.svelte';

	import getCurrentTime from './tools/getTime.js';
	import { startLoading, finishLoading } from './tools/loading.js';

	$ : {
		if ($isLoading) {
			setTimeout( ()=>$isLoading && startLoading(), 500 );
		} else { 
			finishLoading(); 
		}
	}
	const icon = './favicon.png';
	
	let code = writable('우리 잘해보죠\n\n아트록스님 캐리좀 ㅠㅠㅠㅠㅓㅠㅠㅓㅠㅠㅠㅓㅠㅠㅠ\n그레이브즈님 캐리좀 ㅠㅠㅓㅠㅠㅓㅠㅠㅠㅠㅠㅓㅠㅠㅠㅠㅠ\n가렌님 캐리좀 ㅠㅠㅓㅠㅠㅓㅠㅠㅓㅠㅠㅓㅠㅠ\n\n아트록스 갱좀요\n그레이브즈ㅜㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n가렌 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅓㅠㅠㅠㅠㅜㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈 갱좀요\n\n뭐하냐고\n\n팀차이 ㅈㅈ');
	let result = writable('Output of lollang code will be shown here');
	let isError = writable(false);
	let isLoading = writable(false);

	const runCode = async function (e) {
		try {
			$isLoading = true;
			if ($code.includes('리쉬')){ throw "컴파일 모드에서는 '리쉬좀'을 사용할 수 없습니다.\n'캐리좀'을 통해 직접 값을 할당해주세요.\n";}

			// 요청 송신
			const reqUrl = `https://asia-northeast3-lollang-playground.cloudfunctions.net/compileLollang`;
			const reqdata = {
				message : ( ($code.split('\n')).map(line=>line.trim()) ).join('\n'), // 각 코드 라인의 좌/우 공백을 제거(trim)합니다.
			};
			console.log('[req]', reqdata)
			const { data } = await axios.post(reqUrl, JSON.stringify(reqdata)); // { resType, result, pythonCode_raw, pythonCode_postProcessed, compilerVersion }
			
			// 응답 수신
			console.log('[res]', data)
			$result = 	'======== [OUTPUT] ========\n'+data.result
						+'\n\n======== [COMPILED CODE] ========\n'+data.pythonCode_raw.join('\n');
			
			if(data.resType==='SUCCESS'){$isError = false;} 
			else if(data.resType==='ERROR'){
				$isError = true;
				$result = '오류 해결에 lollang github wiki가 도움이 되어드릴 수 있어요\nhttps://github.com/riroan/lollang/wiki/Error\n\n'
							+ $result;
			}
		} catch(err) {
			$result = String(err) + '\n더 많은 정보를 보려면 [F12]를 눌러 개발자 콘솔을 확인해주세요.';
			(String(err)==='Error: Network Error') && ($result+='\n\n인터넷 연결 또는 서버 상태에 이상이 없는 경우, 이 오류는 무한루프에 의해 발생하였을 가능성이 있습니다.\n반복문의 조건식을 확인해주세요.')
			$isError = true;
			console.error(err);
		} finally {
			$isLoading = false;
		}
	}

	const downloadCode = function (e) {
		const blob = new Blob([$code], {
			type: "text/plain;charset=utf-8;",
		});
		saveAs(blob, `lollangCode_${getCurrentTime()}.lo`);
	}
</script>

<div id="app">
	<header>
		<img src={icon} alt={'icon'} />
		<h1 class="header-title">Lollang Playground</h1>
		
		<div class="header-functions" style="margin-left:8px;">
			<SvelteTooltip tip="LEARN" bottom>
				<button class="header-functions-btn" alt="learning materials in lollang github repository"
					on:click={e=>{window.open('https://github.com/riroan/lollang/wiki')}}>
					<span class="material-icons">menu_book</span>
				</button>
			</SvelteTooltip>
			<SvelteTooltip tip="DOWNLOAD CODE" bottom>
				<button class="header-functions-btn" on:click={downloadCode} alt="download code to your computer">
					<span class="material-icons">get_app</span>
				</button>
			</SvelteTooltip>
			<SvelteTooltip tip="RUN CODE" bottom>
				<button class="header-functions-btn runbtn" on:click={runCode} alt="run code">
					<span class="material-icons">flight_takeoff</span>
				</button>
			</SvelteTooltip>
		</div>

		<div class="header-lollang-github" style="margin-left:auto;">
			<button class="header-functions-btn" 
				on:click={e=>{window.open('https://github.com/riroan/lollang')}}>
					lollang GITHUB
			</button>
			<button class="header-functions-btn" 
				on:click={e=>{window.open('https://github.com/wonjinYi/lollang-playground')}}>
					playground GITHUB
			</button>
		</div>
	</header>

	<main>
		<CompileMode {code} {result} {isError}/>
	</main>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap');
	/* @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding&display=swap'); */
	@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
	/* @import url('https://fonts.googleapis.com/css2?family=Material+Icons+Outlined');
	@import url('https://fonts.googleapis.com/css2?family=Material+Icons+Round');
	@import url('https://fonts.googleapis.com/css2?family=Material+Icons+Sharp');
	@import url('https://fonts.googleapis.com/css2?family=Material+Icons+Two+Tone'); */

	:root{
		--gray-strong : #0D1117;
		--gray-normal : rgb(22,27,34);
		--gray-light : rgb(54,59,66);
		--blue-neon : rgb(19,35,58);
		--green-normal : rgb(35,134,54)
	}

	img {
		width : 32px;

		border : 1px solid var(--gray-normal);
		border-radius : 12px;
		background-color : var(--gray-light);
	}

	#app {
		display : flex; 
		flex-direction: column;

		height : 100%;
		width : 100%;

		color : white;
	}

	header {
		display : flex;
		align-items: center;
		
		height : 48px;
		padding : 0 8px;
		z-index : 999;

		background-color : var(--gray-strong);
	}

	.header-title {
		margin : 0;
		margin-left : 4px;

		font-size : 24px;
		font-weight: 200;
		font-family: 'Montserrat', sans-serif;
	}

	.header-functions-btn {
		display : inline-flex;
		align-items : center;
		justify-content: center;

		margin : 0;
		
		background-color : var(--gray-normal);
		color : white;
		font-size : 12px;
		border-radius : 32px;
		border-color : var(--gray-light);
		cursor : pointer;

		transition : background-color 0.2s;
	}
	.header-functions-btn.runbtn {
		background-color : var(--green-normal);
	}
	.header-functions-btn:hover {
		background-color : var(--gray-light);
		transition : background-color 0.2s;
	}
	.header-functions-btn:active {
		background-color : var(--blue-neon);
		transition : background-color 0.2s;
	}

	main {
		display : flex;
		flex : 1;

		width : 100%;
		max-width : 100%;

		border-left : 4px solid var(--gray-strong);
		border-right : 4px solid var(--gray-strong);
		border-bottom : 4px solid var(--gray-strong);
		background-color : var(--gray-normal);
	}
</style>