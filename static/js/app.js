var recibos = angular.module('recibos', []);

recibos.controller('ListaController', function($scope) {
  $scope.recibos = [
    {nombre: 'juan pepe', fecha: 'algun dia'},
    {nombre: 'otro', fecha: 'ayer'},
  ];
});
