<script>
    import { onMount } from 'svelte';
    import * as indentation from 'indent-textarea';
    
    export let code; // store writable

    let lineCounter;
	let highlighter;
	let codeArea;

	const lineCounterWidthBase = 8
	const lineCounterWidthPerChar = 12;
	let lineCounterWidth = lineCounterWidthBase + lineCounterWidthPerChar;

	const onScroll = function () {
		highlighter.scrollTop = codeArea.scrollTop;
    	highlighter.scrollLeft = codeArea.scrollLeft;

		lineCounter.scrollTop = codeArea.scrollTop;
    	lineCounter.scrollLeft = codeArea.scrollLeft;
	}

	const onInput = function () {
		// line counter processing
		let lineCountCache = 0;
		let lineCount = codeArea.value.split('\n').length;
		let outarr = new Array();
		if (lineCountCache != lineCount) {
			for (let x = 0; x < lineCount; x++) {
				outarr[x] = (x + 1);
			}
			lineCounter.value = outarr.join('\n');
		}
		lineCountCache = lineCount;	
		lineCounterWidth = String(lineCountCache).length * lineCounterWidthPerChar + lineCounterWidthBase;
		
		// highlighting
		function applyHighlights(text) {
			text = text
				.replace(/\n$/g, '\n\n')
				.replace(/우리\s잘해보죠|팀차이\sㅈㅈ/g, '<span class="highlight-startend">$&</span>')
				.replace(/\B님\s/g, '<span class="highlight-declarevar">$&</span>')
				.replace(/캐리좀/g, '<span class="highlight-assign">$&</span>')
				.replace(/(?<=ㄴ)(.*?)(?=ㄹ)/g, '<span class="highlight-inner-parentheses">$&</span>')
				.replace(/ㄴ|ㄹ/g, '<span class="highlight-parentheses">$&</span>')
				.replace(/ㄱ|ㅋ|ㄷ|ㅌ/g, '<span class="highlight-compareopr">$&</span>')
				.replace(/ㅜ|ㅡ|ㅓ|ㅏ|ㅕ|ㅑ/g, '<span class="highlight-arithopr">$&</span>')  
				.replace(/갱좀요|갱좀/g, '<span class="highlight-print">$&</span>') 
				.replace(/리쉬좀요|리쉬좀/g, '<span class="highlight-print">$&</span>') 
				.replace(/뭐하냐고/g, '<span class="highlight-newline">$&</span>')
				.replace(/스왑좀/g, '<span class="highlight-changetype">$&</span>')
				.replace(/님아/g, '<span class="highlight-startfor">$&</span>') // for
				.replace(/저기/g, '<span class="highlight-if">$&</span>') // if
				.replace(/근데저기/g, '<span class="highlight-elseif">$&</span>') // if
				.replace(/근데/g, '<span class="highlight-else">$&</span>') // if
				.replace(/그니까/g, '<span class="highlight-while">$&</span>') // while
				.replace(/오라고/g, '<span class="highlight-continue">$&</span>') // while
				.replace(/가라고/g, '<span class="highlight-break">$&</span>') // while
				.replace(/뭐함\?/g, '<span class="highlight-end-controlflow">$&</span>') // end for, while, if 
				.replace(/계속오네/g, '<span class="highlight-declarefunction">$&</span>')
				.replace(/나가라\s그냥/g, '<span class="highlight-void">$&</span>')
				.replace(/진짜/g, '<span class="highlight-callfunction">$&</span>')
				.replace(/\,/g, '<span class="highlight-comma">$&</span>')
				.replace(/\./g, '<span class="highlight-period">$&</span>')
				.replace(/잠만\s|(?<=잠만\s)(.*?)(?=\n)/g, '<span class="highlight-comment">$&</span>');
				
			return text;
		}
		highlighter.innerHTML = applyHighlights(codeArea.value);
	}

	onMount( () => {
		onInput();
        indentation.watch(codeArea);
	})
</script>

<textarea class='line-counter' wrap='off' readonly 
	bind:this={lineCounter}
	style="--lineCounterWidth:{lineCounterWidth}"
/>

<div class='code-container'>
	<div class='highlighter' wrap='off' bind:this={highlighter} ></div>
	<textarea class='code-area' wrap='off' spellcheck='false'
		bind:value={$code} 
		bind:this={codeArea} 
		on:scroll={onScroll}
		on:input={onInput}
	/>
	
</div>


<style>
	.code-container {
		flex : 1;
		position : relative;	
	}

    textarea {
        width : 100%;
		height : 100%;

		margin : 0;

		border-radius : 12px;
		color : white;
        resize: none;
        overflow : auto;

		line-height : 24px;
	}
	textarea:focus {
    	outline: none;
	}
	::-webkit-scrollbar-track{
		border-radius: 10px;
		background-color: var(--gray-strong);
	}
	::-webkit-scrollbar{
		width: 8px;
		height : 1px;
		background-color: var(--gray-strong);
	}
	::-webkit-scrollbar-thumb{
		border-radius: 16px;
		background-color: var(--gray-light);
	}
	::-webkit-scrollbar-corner{
		display : none;
	}
	
    .line-counter {
      	display: flex;

		padding : 8px 4px 8px 4px;
		width: calc( var(--lineCounterWidth) * 1px );

		overflow-y: hidden;
		text-align: right;
		background-color:var(--gray-strong);
		border : 1px solid var(--gray-strong);
		border-radius : 12px 0 0 12px;
		color:var(--gray-lighter);
	}

	.code-area {
		position : absolute;
		padding : 8px 8px 8px 4px;

		background-color : transparent;
		border : 1px solid var(--gray-strong);
		border-radius : 0 12px 12px 0;
		color:transparent;
		caret-color: white;
	}

	.highlighter{
		position : absolute;
		display : inline-block;

		width : 100%;
		height : 100%;

		margin : 0;
		padding : 8px 8px 8px 4px;

		border : 1px solid var(--gray-strong);
		border-radius : 0 12px 12px 0;
		background-color : var(--gray-strong);;
		color : white;
		
		white-space: pre;
		word-wrap: break-word;
		overflow-x:auto;
		line-height : 24px;
		pointer-events : none;
	}

	/* 코드 하이라이팅 색상 */
	:global(.highlight-startend) { color : #85ff7a; }
	:global(.highlight-print) { color : #ffe880; } 
	:global(.highlight-input) { color : #ffe880; } 
	:global(.highlight-newline) { color : #ff6161; }
	:global(.highlight-declarevar) { color : #9cc0ff; }
	:global(.highlight-assign) { color : #9cc0ff; }
	:global(.highlight-parentheses) { color : #80f9ff; }
	:global(.highlight-compareopr) { border : 1px solid white ; }
	:global(.highlight-arithopr) { background-color : #FFFFFF50; }
	:global(.highlight-inner-parentheses) { background-color : #80f9ff50; }
	:global(.highlight-comment) { color : #737373; }
	:global(.highlight-comment > span) { color : #737373; }
	:global(.highlight-changetype) { color : #80f9ff; }
	:global(.highlight-startfor) { color : #ff0ff3; }
	:global(.highlight-if) { color : #ff0ff3; }
	:global(.highlight-elseif) { color : #ff0ff3; }
	:global(.highlight-else) { color : #ff0ff3; }
	:global(.highlight-while) { color : #ff0ff3; }
	:global(.highlight-continue) { color : #ff0ff3; }
	:global(.highlight-break) { color : #ba42ff; }
	:global(.highlight-end-controlflow) { color : #ff0ff3; }
	:global(.highlight-declarefunction) { color : #ff0ff3; }
	:global(.highlight-void) { color : #ba42ff; }
	:global(.highlight-callfunction) { color : #e68e00; }
	:global(.highlight-comma) { }
	:global(.highlight-period) { }
</style> 