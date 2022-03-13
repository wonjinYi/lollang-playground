<script>
    import SvelteTooltip from 'svelte-tooltip';

    export let code;
    export let result;
    export let isError;
</script>

<section class="main-input-part">
    <SvelteTooltip tip="Put your *.lo Code below. And press the green <RUN> button to run it" bottom>
        <h2 class="main-subtitle">CODE</h2>
    </SvelteTooltip>

    <div class="main-article">
        <textarea class="code-editor" placeholder="code your lol here" spellcheck="false" bind:value={$code}/>
    </div>
</section>

<div style="border-right: 2px solid var(--gray-strong);"></div>

<section class="main-output-part">
    <h2 class="main-subtitle">RESULT</h2>
    
    <div class="main-article">
        <textarea class="result-viewer" class:errorMsg={$isError} spellcheck="false" bind:value={$result} readonly></textarea>
    </div>    
</section>

<style>
    section {
		display : flex;
        flex : 1;
		flex-direction: column;
		
		height : 100%;
	}

	.main-subtitle {
		padding-top : 8px;
		margin : 0;

        font-size : 18px;
		font-weight : lighter;
		text-align : center;
	}

	.main-article {
		flex : 1;
		padding : 8px;
	}

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
	.code-editor {
		background-color : var(--gray-strong);
		border : none;
	}
	.result-viewer {
		background-color : var(--gray-normal);;
		border : 2px solid var(--gray-strong);
	}

	.errorMsg {
		color : red;
	}
</style>