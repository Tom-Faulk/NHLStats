<template>
  <div class="container pt-3 pb-5">
    <h2>NHL Players Statistics</h2>
    <b-row>
      <b-col>
        <b-form-input v-model="filterPlayer" type="search" placeholder="Search"></b-form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-table striped hover :items="playerPosts" :fields="playerFields" :sort-by.sync="sortByPlayer" :sort-desc.sync="sortDesc" :filter="filterPlayer" :filter-included-fields="['name']" responsive="sm"></b-table>
        </b-col>
    </b-row>
    <h2>NHL Goalie Statistics</h2>
    <b-row>
      <b-col>
        <b-form-input v-model="filterGoalie" type="search" placeholder="Search"></b-form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-table striped hover :items="goaliePosts" :fields="goalieFields" :sort-by.sync="sortByGoalie" :sort-desc.sync="sortDesc" :filter="filterGoalie" :filter-included-fields="['name']" responsive="sm"></b-table>
        </b-col>
    </b-row>
  </div>
</template>



<script>
export default {
  props: ["playerPosts", "goaliePosts"],
  data() {
    return {
      filterPlayer: "",
      sortByPlayer: 'goals',
      sortDesc: true,
      playerFields: [
        {key: "name", sortable: true},
        {key: "goals", sortable: true},
        {key: "assists", sortable: true},
        {key: 'points', sortable: true}
      ],
      filterGoalie: "",
      sortByGoalie: 'saves',
      goalieFields: [
        {key: "name", sortable: true},
        {key: "saves", sortable: true},
        {key: "shotsAgainst", sortable: true},
        {key: "goalsAgainst", sortable: true},
      ]
    };
  }
};
</script>