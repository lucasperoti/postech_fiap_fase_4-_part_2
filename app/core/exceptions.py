class DomainException(Exception):
    """Base exception for domain errors"""
    pass


class VendaNotFoundException(DomainException):
    pass


class VeiculoNotFoundException(DomainException):
    pass


class VeiculoJaVendidoError(DomainException):
    pass


class PagamentoJaProcessadoError(DomainException):
    pass
