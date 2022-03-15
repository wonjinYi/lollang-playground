<script>
    import { onMount } from 'svelte';
    import * as indentation from 'indent-textarea';
    
    export let code; // store writable

    let lineCounter;
	let codeArea;

	const onScroll = function () {
		lineCounter.scrollTop = codeArea.scrollTop;
    	lineCounter.scrollLeft = codeArea.scrollLeft;
	}

	const onInput = function () {
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
	}

	onMount( () => {
		onInput();
        indentation.watch(codeArea);
	})
</script>

<textarea class='line-counter' wrap='off' readonly bind:this={lineCounter}>1</textarea>

<textarea class='code-area' wrap='off' spellcheck='false'
    bind:value={$code} 
    bind:this={codeArea} 
    on:scroll={onScroll}
    on:input={onInput}
/>

<style>
    textarea {
        width : 100%;
		height : 100%;

		margin : 0;
		padding : 8px;

		border-radius : 12px;
		color : white;
        resize: none;
        overflow : auto;
	}
	textarea:focus {
    	outline: none;
	} 

    .line-counter {
      	display: flex;

		padding-right : 4px;
		width: 36px;

		overflow-y: hidden;
		text-align: right;
		background-color:var(--gray-strong);
		border : 1px solid var(--gray-strong);
		border-radius : 12px 0 0 12px;
		color:var(--gray-lighter);
	}

	.code-area {
		padding-left: 4px;

		background-color : var(--gray-strong);
		border : 2px solid var(--gray-strong);
		border-radius : 0 12px 12px 0;
		color:white;
	}
</style> 