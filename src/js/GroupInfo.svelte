<script>
    import { students_list as students, group_info } from './store';
</script>

<h1 class="box__header"> Информация о группе </h1>
<table class="group_info_table mb-5">
    <tr>
        <th> Всего заявок </th>
        <td> {$students.length} </td>
    </tr>
    <tr>
        <th> План набора </th>
        <td> {$group_info.plan} </td>
    </tr>
    <tr>
        <th> Специальность </th>
        <td> {$group_info.speciality_name} </td>
    </tr>
</table>