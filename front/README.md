# lollang-playground : Frontend

사용자 입력으로 .lo코드를 받고, 서버로  컴파일과 실행을 요청합니다.
실행된 결과는 프론트엔드 상에서 사용자에게 표시됩니다.

컴포넌트 연결 계층

``` 
( src/index.html )
└─ src/main.js
    └─ src/App.svelte
        └─ src/components/CompileMode.svelte
            └─ src/components/CodeEditors.svelte
        └─ (예정) src/components/InteractMode.svelte
            └─ (예정) src/components/CodeEditors.svelte
