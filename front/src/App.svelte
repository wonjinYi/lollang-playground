<script>
	import axios from 'axios';
	import {saveAs} from 'file-saver';
	import SvelteTooltip from 'svelte-tooltip';
	import getCurrentDate from './getData.js';

	const icon = './favicon.png';

	const runCode = async function (e) {
		try {
			const reqUrl = `https://asia-northeast3-lollang-playground.cloudfunctions.net/compileLollang`;
			const reqdata = {
				message : code,
			};
			console.log(reqUrl);
			console.log(JSON.stringify(reqdata));
			const res = await axios.post(reqUrl, JSON.stringify(reqdata));
			console.log(res);
			result = res.data;
		} catch(err) {
			result = err;
			console.error(err);
		}
		
	}

	const downloadCode = function (e) {
		const blob = new Blob([code], {
			type: "text/plain;charset=utf-8;",
		});
		saveAs(blob, `lollangCode_${getCurrentDate()}.lo`);
	}

	let code = '우리 잘해보죠\n\n아트록스님 캐리좀 ㅠㅠㅠㅠㅓㅠㅠㅓㅠㅠㅠㅓㅠㅠㅠ\n그레이브즈님 캐리좀 ㅠㅠㅓㅠㅠㅓㅠㅠㅠㅠㅠㅓㅠㅠㅠㅠㅠ\n가렌님 캐리좀 ㅠㅠㅓㅠㅠㅓㅠㅠㅓㅠㅠㅓㅠㅠ\n\n아트록스 갱좀요\n그레이브즈ㅜㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n가렌 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅓㅠㅠㅠㅠㅜㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈 갱좀요\n\n뭐하냐고\n\n팀차이 ㅈㅈ';
	let result = 'Output of lollang code will be shown here';
	let isError = false;
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
				on:click={e=>{window.open('https://github.com/riroan/lollang')}}>
					playground GITHUB
			</button>
		</div>
	</header>

	<main>
		<section class="main-input-part">
			<SvelteTooltip tip="Put your *.lo Code below. And press the green <RUN> button to run it" bottom>
				<h2 class="main-subtitle">CODE</h2>
			</SvelteTooltip>
			<div class="main-article">
				<textarea class="code-editor" placeholder="code your lol here" spellcheck="false" bind:value={code}/>
			</div>
		</section>
		<div style="border-right: 2px solid var(--gray-strong);"></div>
		<section class="main-output-part">
			<h2 class="main-subtitle">RESULT</h2>
			<div class="main-article">
				<p class="result-viewer">{result}</p>
			</div>
			
		</section>
	</main>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@200&display=swap');
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
		border : 1px solid var(--gray-normal);
		border-radius : 12px;
		background-color : var(--gray-light);

		width : 32px;
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
		border-color : var(--gray-light);
		color : white;
		border-radius : 32px;
		cursor : pointer;
		transition : background-color 0.2s;

		font-size : 12px;
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

	main > section {
		display : flex;
		flex-direction: column;
		flex : 1;
		height : 100%;
	}

	.main-subtitle {
		padding-top : 8px;
		font-size : 18px;
		margin : 0;
		font-weight : lighter;
		text-align : center;
	}

	.main-article {
		flex : 1;
		padding : 8px;
	}

	.code-editor {
		width : 100%;
		height : 100%;
		margin : 0;
		
		resize: none;
		border : none;
		border-radius : 12px;
		background-color : var(--gray-strong);
		color : white;
	}

	.code-editor:focus {
    	outline: none;
	}

	.result-viewer {
		margin : 0;
		word-wrap: break-word;
		font-size : 24px;
		font-weight : 100;
	}
</style>