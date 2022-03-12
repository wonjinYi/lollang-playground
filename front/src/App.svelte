<script>
	import axios from 'axios';
	//const proxy = 'https://cors-anywhere.herokuapp.com/';
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
		console.log('download');
	}

	let code = '우리 잘해보죠\n\n아트록스님 캐리좀 ㅠㅠㅠㅠㅓㅠㅠㅓㅠㅠㅠㅓㅠㅠㅠ\n그레이브즈님 캐리좀 ㅠㅠㅓㅠㅠㅓㅠㅠㅠㅠㅠㅓㅠㅠㅠㅠㅠ\n가렌님 캐리좀 ㅠㅠㅓㅠㅠㅓㅠㅠㅓㅠㅠㅓㅠㅠ\n\n아트록스 갱좀요\n그레이브즈ㅜㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n가렌 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅓㅠㅠㅠㅠㅜㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠㅠㅠㅠ 갱좀요\n그레이브즈ㅜㅠㅠㅓㅠㅠㅠㅠ 갱좀요\n그레이브즈 갱좀요\n\n뭐하냐고\n\n팀차이 ㅈㅈ';
	let result = 'Output of lollang code will be shown here';
	let isError = false;
</script>

<div id="app">
	<header>
		<h1 class="header-title">Lollang Playground</h1>
		<div class="header-functions" style="margin-left:8px;">
			<button class="header-functions-btn" on:click={downloadCode}>DOWNLOAD</button>
			<button class="header-functions-btn" on:click={runCode}>RUN</button>
		</div>
		<div class="header-lollang-github" style="margin-left:auto;">
			<button class="header-functions-btn" 
				on:click={e=>{window.open('https://github.com/riroan/lollang')}}>
					lollang GITHUB
			</button>
		</div>
	</header>

	<main>
		<section class="main-input-part">
			<h2 class="main-subtitle">CODE</h2>
			<div class="main-article">
				<textarea class="code-editor" placeholder="code your lol here" bind:value={code}/>
			</div>
		</section>
		<div style="border-right: 2px solid lightgray;"></div>
		<section class="main-output-part">
			<h2 class="main-subtitle">RESULT</h2>
			<div class="main-article">
				<p class="result-viewer">{result}</p>
			</div>
			
		</section>
	</main>
</div>

<style>
	#app {
		display : flex; 
		flex-direction: column;
		height : 100%;
		width : 100%;
	}

	header {
		display : flex;
		align-items: center;
		
		height : 48px;
		padding : 0 8px;
		background-color : lightgray;
	}

	.header-title {
		margin : 0;
		font-size : 24px;
		font-weight: lighter;
	}

	.header-functions-btn {
		margin : 0;
	}

	main {
		display : flex;
		flex : 1;

		width : 100%;
		max-width : 100%;
		border-left : 4px solid lightgray;
		border-right : 4px solid lightgray;
		border-bottom : 4px solid lightgray;
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
		resize: none;
		border : none;
		width : 100%;
		height : 100%;
		background-color : #ffe0e0;
		margin : 0;
	}

	.code-editor:focus {
    	outline: none;
	}

	.result-viewer {
		margin : 0;
		word-wrap: break-word;
	}
</style>