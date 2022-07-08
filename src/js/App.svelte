<script>
    import InputForm from "./InputForm.svelte";
    import StudentsList from "./StudentsList.svelte";
    import GroupInfo from "./GroupInfo.svelte";
    import { group_info } from './store';
</script>

<div class="box mb-5">
    <InputForm/>
</div>

{#if Object.keys($group_info).length != 0}
    <div class="box mb-5">
        <GroupInfo/>
    </div>
{/if}

<div class="box">
    <StudentsList/>
</div>
